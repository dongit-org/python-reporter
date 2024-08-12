import pytest

import reporter
from reporter import Reporter


def test_document_operations(rc: Reporter) -> None:
    document = rc.documents.create(
        {
            "documentable_type": "Assessment",
            "section": "researcher_briefing",
        },
        file="foo",
    )

    assert rc.documents.get(document.id) == b"foo"

    rc.documents.delete(document.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.documents.get(document.id)
        assert e.value.response_code == 404
