import random

import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers


def create_random_finding_template(rc: Reporter) -> reporter.FindingTemplate:
    title = helpers.rand_alphanum(32)
    description = helpers.rand_alphanum(32)
    finding_template = rc.finding_templates.create(
        {
            "title": title,
            "is_vulnerability": True,
            "description": description,
        }
    )
    assert isinstance(finding_template, reporter.FindingTemplate)
    return finding_template


def test_finding_template_create(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    assert finding_template.id is not None
    rc.finding_templates.get(finding_template.id)


def test_finding_template_delete(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    rc.finding_templates.delete(finding_template.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.finding_templates.get(finding_template.id)
        assert e.value.response_code == 404


def test_finding_template_list(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    finding_templates = rc.finding_templates.list()
    for f in finding_templates:
        if f.id == finding_template.id:
            return
    raise Exception("Finding template not found in list")


def test_finding_template_search(rc: Reporter):
    fts = rc.finding_templates.search("XSS")
    assert len(fts) >= 1


def test_finding_template_get(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    ft = rc.finding_templates.get(finding_template.id)
    assert finding_template == ft


def test_finding_template_update(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    new_title = helpers.rand_alphanum(32)
    updated = rc.finding_templates.update(finding_template.id, {"title": new_title})
    gotten = rc.finding_templates.get(finding_template.id)
    assert finding_template == updated
    assert gotten == updated


def test_finding_template_create_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.finding_templates.create({"asdf": "asdf"})


def test_finding_template_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.finding_templates.get("does-not-exist")


def test_finding_template_update_invalid(rc: Reporter):
    finding_template = create_random_finding_template(rc)
    with pytest.raises(reporter.ReporterHttpError):
        rc.finding_templates.update(finding_template.id, {"title": None})
