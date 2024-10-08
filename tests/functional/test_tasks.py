from typing import cast

import pytest

import reporter
from reporter import Reporter, Assessment, AssessmentUser, Task


@pytest.fixture(scope="session")
def assessment(rc: Reporter) -> Assessment:
    client = rc.clients.create(
        {
            "name": "test_tasks",
            "description": "foo",
        }
    )

    assessment_template = rc.assessment_templates.list()[0]

    assessment = client.assessments.create(
        {
            "title": "test_tasks",
            "assessment_template_id": assessment_template.id,
        }
    )
    return cast(Assessment, assessment)


@pytest.fixture(scope="session")
def assessment_user(rc: Reporter, assessment: Assessment) -> AssessmentUser:
    user = rc.users.create(
        {
            "first_name": "Assessment",
            "last_name": "User",
            "email": "test_tasks@example.com",
            "roles": ["admin"],
        }
    )
    assessment_user = assessment.users.create({"user_id": user.id, "type": 1})
    return cast(AssessmentUser, assessment_user)


def test_task_operations(rc: Reporter, assessment: Assessment) -> None:
    task = assessment.tasks.create(
        {
            "deadline_type": 5,
            "weight": 12345,
            "data": {
                "title": "task title",
                "description": "task description",
            },
        }
    )

    assert task in rc.tasks.list(filter={"id": task.id})

    rc.tasks.update(task.id, {"weight": 24680})
    gotten = rc.tasks.get(task.id)

    assert task == gotten
    for attr in ["deadline_type", "data"]:
        assert getattr(task, attr) == getattr(gotten, attr)
    assert gotten.weight == 24680

    rc.tasks.delete(task.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.tasks.get(task.id)
        assert e.value.response_code == 404


def test_task_set_operations(
    rc: Reporter, assessment: Assessment, assessment_user: AssessmentUser
) -> None:
    task_set = rc.task_sets.create(
        {
            "deadline_type": 5,
            "name": "task set",
            "tasks": [
                {
                    "title": f"Task {i}",
                    "description": f"Task number {i}",
                    "weight": i * 100,
                }
                for i in range(1, 6)
            ],
        }
    )

    assert task_set in rc.task_sets.list(filter={"id": task_set.id})

    rc.task_sets.update(task_set.id, {"name": "Task set! 123"})
    gotten = rc.task_sets.get(task_set.id)

    assert task_set == gotten
    for attr in ["deadline_type", "tasks"]:
        assert getattr(task_set, attr) == getattr(gotten, attr)

    tasks = assessment.task_sets.create(
        {
            "task_set_id": task_set.id,
            "assigned_users": [assessment_user.user_id],
        }
    )

    assert isinstance(tasks, list)
    assert isinstance(tasks[0], Task)
    assert tasks[0].data["title"] == "Task 1"

    assessment.task_sets.delete(task_set.id)

    rc.task_sets.delete(task_set.id)
    with pytest.raises(reporter.ReporterHttpError) as e:
        rc.task_sets.get(task_set.id)
        assert e.value.response_code == 404
