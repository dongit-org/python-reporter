# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin


__all__ = [
    "Task",
    "TaskManager",
    "AssessmentTaskManager",
]


class Task(RestObject):
    pass


class TaskManager(RestManager, DeleteMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "tasks"
    _obj_cls = Task


class AssessmentTaskManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/tasks"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Task
