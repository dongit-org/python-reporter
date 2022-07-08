import random

import pytest  # type: ignore

import reporter
from reporter import Reporter
from reporter.objects import assessment

from . import helpers
from .test_client import create_random_client


def get_random_assessment_type_id(rc: Reporter) -> str:
    types = rc.assessment_types.list()
    return random.choice(types).id


def create_random_assessment(
    rc: Reporter, client: reporter.Client
) -> reporter.Assessment:
    assessment_type_id = get_random_assessment_type_id(rc)
    title = helpers.rand_alphanum(32)
    assessment = client.assessments.create(
        {
            "assessment_type_id": assessment_type_id,
            "title": title,
        }
    )
    assert isinstance(assessment, reporter.Assessment)
    return assessment


def test_assessment_create(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    assert assessment.id is not None


def test_assessment_list(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    assessments = rc.assessments.list()
    for a in assessments:
        if a.id == assessment.id:
            return
    raise Exception("Assessment not found in list")


def test_assessment_get(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    a = rc.assessments.get(assessment.id)
    assert assessment == a


def test_assessment_update(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    new_title = helpers.rand_alphanum(32)
    updated = rc.assessments.update(assessment.id, {"title": new_title})
    gotten = rc.assessments.get(assessment.id)
    assert assessment == updated
    assert gotten == updated


def test_assessment_create_invalid(rc: Reporter):
    client = create_random_client(rc)
    with pytest.raises(reporter.ReporterHttpError):
        client.assessments.create({"asdf": "asdf"})


def test_assessment_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.assessments.get("does-not-exist")


def test_assessment_update_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    with pytest.raises(reporter.ReporterHttpError):
        rc.assessments.update(assessment.id, {"status": None})
