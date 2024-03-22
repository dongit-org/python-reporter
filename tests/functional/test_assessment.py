import os

import pytest  # type: ignore

import reporter
from reporter import Reporter


@pytest.fixture(scope="session")
def client(rc: Reporter) -> reporter.Client:
    client = rc.clients.create(
        {
            "name": "test_assessment",
            "description": "foo",
        }
    )
    return client


@pytest.fixture(scope="session")
def assessment_template(rc: Reporter) -> reporter.AssessmentTemplate:
    template = rc.assessment_templates.list()[0]
    return template


def test_assessment_operations(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_assessment_operations",
            "assessment_template_id": assessment_template.id,
        }
    )

    assert assessment in rc.assessments.list(filter={"id": assessment.id})

    rc.assessments.update(assessment.id, {"internal_details": "foo"})
    gotten = rc.assessments.get(assessment.id)

    assert assessment == gotten
    for attr in ["title", "description"]:
        assert getattr(assessment, attr) == getattr(gotten, attr)
    assert gotten.internal_details == "foo"


def test_assessment_comments_and_replies(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_assessment_comments_and_replies",
            "assessment_template_id": assessment_template.id,
        }
    )

    assert assessment in rc.assessments.list(filter={"id": assessment.id})

    assessment.comments.create(
        {
            "body": "Private comment",
            "is_private": True,
        }
    )
    comments = rc.assessments.get(assessment.id, include=["comments"]).comments
    comment = next(
        (c for c in comments if c.body == "Private comment" and c.is_private), None
    )
    assert comment is not None

    rc.assessment_comments.update(
        comment.id, {"body": "Public comment", "is_private": False}
    )
    comments = rc.assessments.get(assessment.id, include=["comments"]).comments
    comment = next(
        (c for c in comments if c.body == "Public comment" and not c.is_private), None
    )
    assert comment is not None

    rc.assessment_comments.delete(comment.id)
    comments = rc.assessments.get(assessment.id, include=["comments"]).comments
    assert not any(c for c in comments if c.id == comment.id)


def test_assessment_phases_and_sections(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_assessment_phases_and_sections",
            "assessment_template_id": assessment_template.id,
        }
    )

    phase_update = {
        "research_start_date": "1970-01-01",
        "research_deadline": "1970-01-02",
    }

    phase = rc.assessments.get(assessment.id, include=["phases"]).phases[0]
    rc.assessment_phases.update(phase.id, phase_update)
    phase = rc.assessments.get(assessment.id, include=["phases"]).phases[0]

    for attr, val in phase_update.items():
        assert getattr(phase, attr) == val

    section_update = {
        "name": "foo",
        "description": "bar",
    }

    section = rc.assessments.get(assessment.id, include=["sections"]).sections[0]
    rc.assessment_sections.update(section.id, section_update)
    section = rc.assessments.get(assessment.id, include=["sections"]).sections[0]

    for attr, val in section_update.items():
        assert getattr(section, attr) == val


def test_assessment_users(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_assessment_users",
            "assessment_template_id": assessment_template.id,
        }
    )

    user = rc.users.create(
        {
            "first_name": "First",
            "last_name": "Last",
            "email": "test_assessment_users@example.com",
            "roles": ["admin"],
        }
    )
    assessment_user = assessment.users.create({"user_id": user.id, "type": 1})
    assessment.users.update(user.id, {"type": 2})
    assessment_user = rc.assessments.get(
        assessment.id, include=["assessmentUsers"]
    ).assessmentUsers[0]

    assert assessment_user.user_id == user.id
    assert assessment_user.type == 2


def test_activities(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_activities",
            "assessment_template_id": assessment_template.id,
        }
    )

    target = assessment.targets.create(
        {
            "target_type": 1,
            "name": "test_activities",
        }
    )
    section = [
        s
        for s in rc.assessments.get(assessment.id, include=["sections"]).sections
        if s.can_have_findings
    ][0]
    finding = assessment.findings.create(
        {
            "title": "test_activities",
            "targets": [target.id],
            "assessment_section_id": section.id,
            "is_vulnerability": False,
            "description": "foo",
        }
    )

    activity = rc.activities.list(
        filter={
            "assessment_id": assessment.id,
            "type": "40",
        }
    )[0]
    assert activity.assessment_id == assessment.id
    assert activity.finding_id == finding.id


def test_output_files(rc: Reporter, client, assessment_template):
    assessment = client.assessments.create(
        {
            "title": "test_output_files",
            "assessment_template_id": assessment_template.id,
        }
    )

    with open(
        f"{os.path.dirname(os.path.abspath(__file__))}/output_file.json", "r"
    ) as f:
        output_file_contents = f.read()

    output_file = assessment.output_files.create(
        {
            "name": "output_file_test",
            "tool": "generic",
        },
        file=output_file_contents,
    )

    gotten = rc.assessments.get(assessment.id, include=["outputFiles"]).outputFiles[0]
    assert output_file == gotten
    assert gotten.name == "output_file_test"
    assert gotten.tool == "generic"

    rc.output_files.delete(output_file.id)
    assert (
        len(rc.assessments.get(assessment.id, include=["outputFiles"]).outputFiles) == 0
    )
