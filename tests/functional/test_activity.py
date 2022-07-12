from reporter import Reporter

from .test_client import create_random_client
from .test_assessment import create_random_assessment


def test_activity_list(rc: Reporter):
    client = create_random_client(rc)
    assessment = create_random_assessment(rc, client)
    activities = rc.activities.list(filter={"assessment_id": assessment.id})
    assert len(activities) == 1
