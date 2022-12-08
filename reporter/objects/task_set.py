# pylint: disable = missing-module-docstring, missing-class-docstring

from typing import List
from reporter.base import RestManager, RestObject, Reporter
from reporter.mixins import CreateMixin, CrudMixin, DeleteMixin, ListMixin
from reporter.objects.task import Task


__all__ = [
    "TaskSet",
    "TaskSetManager",
    "AssessmentTaskSetManager",
]


class TaskSet(RestObject):
    pass


class TaskSetManager(RestManager, CrudMixin, ListMixin):
    _path = "task-sets"
    _obj_cls = TaskSet


class AssessmentTaskSetManager(RestManager, CreateMixin, DeleteMixin):
    _path = "assessments/{assessment_id}/task-sets"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = List[Task]

    def _obj_cast(self, reporter: Reporter, tasks: List):
        return [Task(reporter, task) for task in tasks]
