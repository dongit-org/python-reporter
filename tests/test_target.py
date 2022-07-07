import random

import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers
from .test_client import create_random_client
from .test_assessment import create_random_assessment


def create_random_target(assessment: reporter.Assessment) -> reporter.Target:
    name = helpers.rand_alphanum(32)
    target_type = random.randint(0, 6)
    target = assessment.targets.create(
        {
            "name": name,
            "target_type": target_type,
        }
    )
    assert isinstance(target, reporter.Target)
    return target


def test_target_create(rc: Reporter):
    n = len(rc.targets.list())
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    assert target.id is not None
    assert len(rc.targets.list()) == n + 1


def test_target_delete(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    rc.targets.delete(target.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.targets.get(target.id)
        assert e.value.response_code == 404


def test_target_list(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    targets = rc.targets.list()
    for t in targets:
        if t.id == target.id:
            return
    raise Exception("Target not found in list")


def test_target_get(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    t = rc.targets.get(target.id)
    assert target == t


def test_target_update(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    new_name = helpers.rand_alphanum(32)
    updated = rc.targets.update(target.id, {"name": new_name})
    gotten = rc.targets.get(target.id)
    assert target == updated
    assert gotten == updated


def test_target_create_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    with pytest.raises(reporter.ReporterHttpError):
        assessment.targets.create({"asdf": "asdf"})


def test_target_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.targets.get("does-not-exist")


def test_target_update_invalid(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    target = create_random_target(assessment)
    with pytest.raises(reporter.ReporterHttpError):
        rc.targets.update(target.id, {"name": None})
