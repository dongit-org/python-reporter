import pytest  # type: ignore
from uuid import uuid4

import reporter
from reporter import Reporter


def test_webhook_operations(rc: Reporter):
    webhook = rc.webhooks.create(
        {
            "url": "https://example.com/webhooks/1",
            "name": "onAssessmentCreated",
            "secret": str(uuid4()),
            "types": ["assessment:created"],
            "mode": 1,
        }
    )

    rc.webhooks.delete(webhook.id)

    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.webhooks.delete(webhook.id)
        assert e.value.response_code == 404
