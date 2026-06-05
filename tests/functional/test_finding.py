from typing import cast

import pytest

import reporter
from reporter import (
    Reporter,
    Assessment,
    AssessmentSection,
    FindingComment,
    FindingCreatedEvent,
    FindingPublishedEvent,
    FindingRetest,
    FindingRetestInquiry,
    Target,
)

from .utils import Artisan, wait_for


@pytest.fixture(scope="session")
def assessment(rc: Reporter) -> Assessment:
    client = rc.clients.create(
        {
            "name": "test_finding",
            "description": "foo",
        }
    )
    assessment_template = rc.assessment_templates.list()[0]
    assessment = client.assessments.create(
        {
            "title": "test_finding",
            "assessment_template_id": assessment_template.id,
        }
    )
    rc.assessments.update(assessment.id, {"scoring_system": "owasp"})
    return cast(Assessment, rc.assessments.get(assessment.id, include=["sections"]))


@pytest.fixture(scope="session")
def target(rc: Reporter, assessment: Assessment) -> Target:
    return cast(
        Target,
        assessment.targets.create(
            {
                "target_type": 0,
                "name": "example.com",
            }
        ),
    )


@pytest.fixture(scope="session")
def section(rc: Reporter, assessment: Assessment) -> AssessmentSection:
    section = assessment.sections[0]
    rc.assessment_sections.update(
        section.id,
        {
            "can_have_findings": True,
        },
    )
    return cast(AssessmentSection, section)


def test_target_operations(rc: Reporter, assessment: Assessment) -> None:
    target = assessment.targets.create(
        {
            "target_type": 0,
            "name": "test_target_operations",
        }
    )

    assert target in rc.targets.list(filter={"id": target.id})

    rc.targets.update(target.id, {"description": "foo"})
    gotten = rc.targets.get(target.id)

    assert target == gotten
    for attr in ["target_type", "name"]:
        assert getattr(target, attr) == getattr(gotten, attr)
    assert gotten.description == "foo"

    rc.targets.delete(target.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.targets.get(target.id)
        assert e.value.response_code == 404


def test_finding_operations(rc: Reporter, assessment: Assessment) -> None:
    target = assessment.targets.create(
        {
            "target_type": 0,
            "name": "test_finding_operations",
        }
    )
    section = [
        s
        for s in rc.assessments.get(assessment.id, include=["sections"]).sections
        if s.can_have_findings
    ][0]

    finding = assessment.findings.create(
        {
            "title": "test_finding_operations",
            "targets": [target.id],
            "assessment_section_id": section.id,
            "is_vulnerability": False,
            "severity": 1,
            "description": "foo",
            "review_status": 0,
            "is_published": False,
        }
    )

    assert finding in rc.findings.list(filter={"id": finding.id})

    rc.findings.update(finding.id, {"description": "bar"})
    gotten = rc.findings.get(finding.id)

    assert finding == gotten
    for attr in [
        "title",
        "assessment_section_id",
        "is_vulnerability",
        "review_status",
        "is_published",
    ]:
        assert getattr(finding, attr) == getattr(gotten, attr)
    assert gotten.description == "bar"

    rc.findings.delete(finding.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.findings.get(finding.id)
        assert e.value.response_code == 404


def test_finding_template_operations(
    rc: Reporter, assessment: Assessment, section: AssessmentSection, target: Target
) -> None:
    # The seeded finding templates are indexed asynchronously by Horizon
    # (Scout queue), so the search may not return results immediately after
    # the stack comes up.
    def xss_template_indexed() -> None:
        assert len(rc.finding_templates.search("XSS")) > 0

    wait_for(xss_template_indexed, timeout=20, interval=1)

    template = rc.finding_templates.create(
        {
            "primary_language_id": "en",
            "title": "test_finding_template_operations",
            "is_vulnerability": False,
            "severity": 3,
            "description": "foo",
        }
    )

    assert template in rc.finding_templates.list(filter={"id": template.id})

    rc.finding_templates.update(template.id, {"risk": "bar"})
    gotten = rc.finding_templates.get(template.id)

    assert template == gotten
    for attr in ["title", "is_vulnerability", "description"]:
        assert getattr(template, attr) == getattr(gotten, attr)
    assert gotten.risk == "bar"

    finding = assessment.findings.create_from_template(
        template.id,
        {
            "assessment_section_id": section.id,
            "targets": [target.id],
        },
    )
    gotten = rc.findings.get(finding.id)
    assert finding == gotten
    for attr in ["title", "risk", "description"]:
        assert getattr(finding, attr) == getattr(gotten, attr)

    with_languages = rc.finding_templates.get(template.id, include=["languages"])
    assert hasattr(with_languages, "languages")

    rc.finding_templates.delete(template.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.finding_templates.get(template.id)
        assert e.value.response_code == 404


def test_finding_template_translations(rc: Reporter, artisan: Artisan) -> None:
    # Ensure a second language exists so we can translate into it.
    artisan.execute(
        "\\App\\Models\\Language::firstOrCreate("
        '["language" => "nl"], '
        '["name" => "Dutch", "translated_name" => "Nederlands"]'
        ");"
    )

    template = rc.finding_templates.create(
        {
            "primary_language_id": "en",
            "title": "test_finding_template_translations_en",
            "is_vulnerability": False,
            "severity": 3,
            "description": "English description",
        }
    )

    # Translatable models without a dedicated add-translation route create the
    # translation implicitly on update when ``language_id`` references a language
    # the model has not been translated into yet.
    rc.finding_templates.update(
        template.id,
        {
            "language_id": "nl",
            "title": "test_finding_template_translations_nl",
            "description": "Nederlandse beschrijving",
        },
    )

    in_nl = rc.finding_templates.get(template.id, query_data={"language_id": "nl"})
    assert in_nl.title == "test_finding_template_translations_nl"
    assert in_nl.description == "Nederlandse beschrijving"
    assert "nl" in in_nl.language_ids
    assert "en" in in_nl.language_ids

    in_en = rc.finding_templates.get(template.id, query_data={"language_id": "en"})
    assert in_en.title == "test_finding_template_translations_en"

    listed_any = rc.finding_templates.list(
        filter={"id": template.id, "language_ids": "nl"}
    )
    assert template in listed_any
    listed_all = rc.finding_templates.list(
        filter={"id": template.id, "and_language_ids": "en,nl"}
    )
    assert template in listed_all

    rc.finding_templates.delete(template.id)


def test_finding_event_operations(
    rc: Reporter, assessment: Assessment, section: AssessmentSection, target: Target
) -> None:
    finding = assessment.findings.create(
        {
            "title": "test_finding",
            "targets": [target.id],
            "assessment_section_id": section.id,
            "is_vulnerability": True,
            "severity_metrics": {
                "impact": 1,
                "likelihood": 1,
                "scoring_system": "owasp",
            },
            "description": "foo",
            "review_status": 0,
            "is_published": False,
        }
    )

    rc.findings.update(
        finding.id,
        {
            "status": 0,
            "review_status": 2,
            "is_published": True,
        },
    )

    # Create comments and replies
    comment = finding.comments.create({"body": "Finding comment"})
    reply = comment.replies.create({"body": "Reply to comment"})
    finding = rc.findings.get(finding.id, include=["comments.replies"])
    comment = next(c for c in finding.comments if c.id == comment.id)
    assert comment is not None and comment.body == "Finding comment"
    reply = next(r for r in comment.replies if r.id == reply.id)
    assert reply is not None and reply.body == "Reply to comment"

    # Update comments and replies
    rc.finding_comments.update(comment.id, {"body": "Updated comment"})
    rc.finding_comments.update(reply.id, {"body": "Updated reply"})
    finding = rc.findings.get(finding.id, include=["comments.replies"])
    comment = next(c for c in finding.comments if c.id == comment.id)
    assert comment is not None and comment.body == "Updated comment"
    reply = next(r for r in comment.replies if r.id == reply.id)
    assert reply is not None and reply.body == "Updated reply"

    # List finding events
    events = rc.finding_events.list(filter={"finding_id": finding.id})
    assert any(e for e in events if isinstance(e, FindingCreatedEvent))
    assert any(event for event in events if isinstance(event, FindingPublishedEvent))
    assert any(
        event
        for event in events
        if isinstance(event, FindingComment) and event.body == "Updated comment"
    )
    assert any(
        event
        for event in events
        if isinstance(event, FindingComment)
        and event.body == "Updated reply"
        and event.parent_id == comment.id
    )
    assert len(events) == 4

    # Delete comments and replies
    rc.finding_comments.delete(reply.id)
    finding = rc.findings.get(finding.id, include=["comments.replies"])
    comment = next(c for c in finding.comments if c.id == comment.id)
    assert comment is not None
    assert len(comment.replies) == 0
    rc.finding_comments.delete(comment.id)
    finding = rc.findings.get(finding.id, include=["comments.replies"])
    assert not any(c for c in finding.comments if c.id == comment.id)

    # Create finding retest inquiries
    inquiry = finding.retestInquiries.create({"body": "New inquiry!"})
    finding = rc.findings.get(finding.id, include=["retestInquiries"])
    assert finding.status == 2
    assert finding.retestInquiries[0].body == "New inquiry!"

    # Update finding retest inquiries
    rc.finding_retest_inquiries.update(inquiry.id, {"body": "Updated inquiry"})
    finding = rc.findings.get(finding.id, include=["retestInquiries"])
    inquiry = finding.retestInquiries[0]
    assert inquiry.body == "Updated inquiry"

    # Delete finding retest inquiries
    rc.finding_retest_inquiries.delete(inquiry.id)
    finding = rc.findings.get(finding.id, include=["retestInquiries"])
    assert len(finding.retestInquiries) == 0

    # Create retests
    finding.retestInquiries.create({"body": "New inquiry!"})
    finding.retests.create(
        {"status": 1, "review_status": 0, "is_published": False, "body": "TODO"}
    )
    retest = rc.findings.get(finding.id, include=["retests"]).retests[0]
    assert retest.body == "TODO"

    # Update retests
    rc.finding_retests.update(retest.id, {"body": "Solved", "review_status": 2})
    retest = rc.findings.get(finding.id, include=["retests"]).retests[0]
    assert retest.body == "Solved"

    # List more finding events
    events = rc.finding_events.list(filter={"finding_id": finding.id})
    assert any(e for e in events if isinstance(e, FindingCreatedEvent))
    assert any(event for event in events if isinstance(event, FindingPublishedEvent))
    assert any(
        event
        for event in events
        if isinstance(event, FindingRetestInquiry) and event.body == "New inquiry!"
    )
    assert any(e for e in events if isinstance(e, FindingRetest) and e.body == "Solved")
    assert len(events) == 4

    # Delete retests
    rc.finding_retests.delete(retest.id)
    assert len(rc.findings.get(finding.id, include=["retests"]).retests) == 0

    rc.findings.delete(finding.id)
