import pytest  # type: ignore

import reporter
from reporter import Reporter

from . import helpers


def create_random_document(rc: Reporter) -> reporter.Document:
    document = rc.documents.create(
        {
            "documentable_type": "Finding",
            "section": "description",
        },
        file=helpers.rand_alphanum(32),
    )
    assert isinstance(document, reporter.Document)
    return document


def test_document_create(rc: Reporter):
    document = create_random_document(rc)
    assert document.id is not None
    rc.documents.get(document.id)


def test_document_get(rc: Reporter):
    contents = helpers.rand_alphanum(32).encode()
    document = rc.documents.create(
        {
            "documentable_type": "Finding",
            "section": "description",
        },
        file=contents,
    )
    d = rc.documents.get(document.id)
    assert contents == d


def test_document_create_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        # No file upload
        rc.documents.create(
            {
                "documentable_type": "Finding",
                "section": "description",
            },
        )


def test_document_get_invalid(rc: Reporter):
    with pytest.raises(reporter.ReporterHttpError):
        rc.documents.get("does-not-exist")
