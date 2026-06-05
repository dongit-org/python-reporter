from typing import cast

import pytest

import reporter
from reporter import (
    Reporter,
    Assessment,
    AssessmentSection,
    Target,
)


@pytest.fixture(scope="session")
def assessment(rc: Reporter) -> Assessment:
    client = rc.clients.create(
        {
            "name": "test_finding_retest_cancelled_event",
            "description": "foo",
        }
    )
    assessment_template = rc.assessment_templates.list()[0]
    assessment = client.assessments.create(
        {
            "title": "test_finding_retest_cancelled_event",
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


def test_finding_retest_cancelled_event_operations(
    rc: Reporter, assessment: Assessment, section: AssessmentSection, target: Target
) -> None:
    finding = assessment.findings.create(
        {
            "title": "test_finding_retest_cancelled_event_operations",
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
        finding.id, {"status": 0, "review_status": 2, "is_published": True}
    )

    finding.retestInquiries.create({"body": "Retest please"})

    inquiry = rc.findings.get(finding.id, include=["retestInquiries"]).retestInquiries[
        0
    ]
    cancelled = inquiry.retestCancelledEvents.create({"body": "Cancelled"})
    assert cancelled.body == "Cancelled"

    rc.finding_retest_cancelled_events.update(cancelled.id, {"body": "Updated"})
    refreshed = rc.findings.get(
        finding.id, include=["retestCancelledEvents"]
    ).retestCancelledEvents[0]
    assert refreshed.body == "Updated"

    rc.finding_retest_cancelled_events.delete(cancelled.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.finding_retest_cancelled_events.delete(cancelled.id)
        assert e.value.response_code == 404
