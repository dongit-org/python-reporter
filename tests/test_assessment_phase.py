import pytest  # type: ignore

import reporter
from reporter import Reporter

from .test_client import create_random_client
from .test_assessment import create_random_assessment


def test_assessment_type_update(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    phase = rc.assessments.get(assessment.id, includes=["phases"]).phases[0]
    updated = rc.assessment_phases.update(
        phase.id,
        {"research_start_date": "1970-01-01", "research_deadline": "1970-01-02"},
    )
    gotten = rc.assessments.get(assessment.id, includes=["phases"]).phases[0]
    assert phase == updated
    assert gotten == updated
    assert gotten.research_start_date == "1970-01-01"


def test_assessment_type_update_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    phase = rc.assessments.get(assessment.id, includes=["phases"]).phases[0]
    with pytest.raises(reporter.ReporterHttpError):
        rc.assessment_phases.update(phase.id, {"visible_on_report": "asdf"})
