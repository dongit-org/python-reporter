import pytest  # type: ignore

import reporter
from reporter import Reporter


def test_assessment_type_list(rc: Reporter):
    rc.assessment_types.list()


def test_assessment_type_get(rc: Reporter):
    types = rc.assessment_types.list()
    for t in types:
        type = rc.assessment_types.get(t.id)
        assert type.id is not None


def test_assessment_type_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.assessment_types.get("does-not-exist")
