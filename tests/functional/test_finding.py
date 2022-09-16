import pytest  # type: ignore

import reporter
from reporter import Reporter


@pytest.fixture(scope="session")
def assessment(rc: Reporter) -> reporter.Client:
    client = rc.clients.create(
        {
            "name": "test_finding",
            "description": "foo",
        }
    )
    assessment_type = rc.assessment_types.list()[0]
    assessment = client.assessments.create(
        {
            "title": "test_finding",
            "assessment_type_id": assessment_type.id,
        }
    )
    return assessment


def test_target_operations(rc: Reporter, assessment):
    target = assessment.targets.create(
        {
            "target_type": 0,
            "name": "test_target_operations",
        }
    )

    assert target in rc.targets.list(filter_={"id": target.id})

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


def test_finding_operations(rc: Reporter, assessment):
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
            "description": "foo",
        }
    )

    assert finding in rc.findings.list(filter_={"id": finding.id})

    rc.findings.update(finding.id, {"description": "bar"})
    gotten = rc.findings.get(finding.id)

    assert finding == gotten
    for attr in ["title", "assessment_section_id", "is_vulnerability"]:
        assert getattr(finding, attr) == getattr(gotten, attr)
    assert gotten.description == "bar"

    rc.findings.delete(finding.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.findings.get(finding.id)
        assert e.value.response_code == 404


def test_finding_template_operations(rc: Reporter):
    assert len(rc.finding_templates.search("XSS")) > 0

    template = rc.finding_templates.create(
        {
            "title": "test_finding_template_operations",
            "is_vulnerability": False,
            "severity": 3,
            "description": "foo",
        }
    )

    assert template in rc.finding_templates.list(filter_={"id": template.id})

    rc.finding_templates.update(template.id, {"risk": "bar"})
    gotten = rc.finding_templates.get(template.id)

    assert template == gotten
    for attr in ["title", "is_vulnerability", "description"]:
        assert getattr(template, attr) == getattr(template, attr)
    assert gotten.risk == "bar"

    rc.finding_templates.delete(template.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.finding_templates.get(template.id)
        assert e.value.response_code == 404
