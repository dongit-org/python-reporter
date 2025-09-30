from typing import Generator, cast
import pytest
from .utils import Artisan
from reporter import Reporter, Assessment


@pytest.fixture
def assessment(rc: Reporter, artisan: Artisan) -> Generator[Assessment, None, None]:
    # By default, assessments do not have checklists, and we can't create one using the API, so we must use Artisan
    artisan.execute(
        """
        $assessment = \\App\\Models\\Assessment::factory()
            ->withChecklists()
            ->create(['title' => 'test_checklist']);
        """
    )

    assessments = rc.assessments.list(filter={"title": "test_checklist"})
    assert len(assessments) == 1
    assessment = cast(Assessment, assessments[0])

    yield assessment

    # Clean up
    rc.assessments.delete(assessment.id, post_data={"explanation": "test cleanup"})


def test_test_case_operations(rc: Reporter, assessment: Assessment) -> None:
    assessment = rc.assessments.get(assessment.id, include="testCases")

    assert len(assessment.testCases) > 0
    test_case = assessment.testCases[0]

    rc.test_cases.update(test_case.id, {"explicit_result": 2})
    gotten = rc.test_cases.get(test_case.id)

    assert gotten == test_case
    assert gotten.description == test_case.description
    assert gotten.result == 2
