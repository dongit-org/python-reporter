import random

import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers
from .test_client import create_random_client
from .test_assessment import create_random_assessment
from .test_target import create_random_target


def get_random_assessment_section_id(
    rc: Reporter, assessment: reporter.Assessment
) -> str:
    sections = rc.assessments.get(assessment.id, includes=["sections"]).sections
    sections = [s for s in sections if s.can_have_findings]
    return random.choice(sections).id


def create_random_finding(
    rc: Reporter, assessment: reporter.Assessment
) -> reporter.Finding:
    for _ in range(5):
        create_random_target(assessment)
    targets = random.sample(rc.targets.list(filter={"assessment_id": assessment.id}), 3)
    title = helpers.rand_alphanum(32)
    description = helpers.rand_alphanum(32)
    assessment_section_id = get_random_assessment_section_id(rc, assessment)
    finding = assessment.findings.create(
        {
            "title": title,
            "description": description,
            "targets": [t.id for t in targets],
            "assessment_section_id": assessment_section_id,
            "is_vulnerability": False,
        }
    )
    assert isinstance(finding, reporter.Finding)
    return finding


def test_finding_create(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    assert finding.id is not None


def test_finding_delete(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    rc.findings.delete(finding.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.findings.get(finding.id)
        assert e.value.response_code == 404


def test_finding_list(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    findings = rc.findings.list()
    for f in findings:
        if f.id == finding.id:
            return
    raise Exception("Finding not found in list")


def test_finding_get(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    f = rc.findings.get(finding.id)
    assert finding == f


def test_finding_update(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    new_title = helpers.rand_alphanum(32)
    updated = rc.findings.update(finding.id, {"title": new_title})
    gotten = rc.findings.get(finding.id)
    assert finding == updated
    assert gotten == updated


def test_finding_create_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    with pytest.raises(reporter.ReporterHttpError):
        assessment.findings.create({"asdf": "asdf"})


def test_finding_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.findings.get("does-not-exist")


def test_finding_update_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    with pytest.raises(reporter.ReporterHttpError):
        rc.findings.update(finding.id, {"title": None})
