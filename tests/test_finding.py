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
    sections = [s for s in sections if s["can_have_findings"]]
    return random.choice(sections)["id"]


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
    n = len(rc.findings.list())
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    finding = create_random_finding(rc, assessment)
    assert finding.id is not None
    assert len(rc.findings.list()) == n + 1


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
    assert f.id is not None


def test_finding_create_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    with pytest.raises(reporter.ReporterHttpError):
        assessment.findings.create({"asdf": "asdf"})


def test_finding_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.findings.get("does-not-exist")
