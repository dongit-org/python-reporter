# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.assessment_user import AssessmentAssessmentUserManager
from reporter.objects.finding import AssessmentFindingManager
from reporter.objects.output_file import AssessmentOutputFileManager
from reporter.objects.target import AssessmentTargetManager
from reporter.objects.task import AssessmentTaskManager
from reporter.objects.task_set import AssessmentTaskSetManager


__all__ = [
    "Assessment",
    "AssessmentManager",
    "ClientAssessmentManager",
]


class Assessment(RestObject):
    _children = {
        "findings": AssessmentFindingManager,
        "output_files": AssessmentOutputFileManager,
        "targets": AssessmentTargetManager,
        "tasks": AssessmentTaskManager,
        "task_sets": AssessmentTaskSetManager,
        "users": AssessmentAssessmentUserManager,
    }


class AssessmentManager(RestManager, GetMixin, ListMixin, UpdateMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RestManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
