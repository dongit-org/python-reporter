# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.assessment_user import AssessmentAssessmentUserManager
from reporter.objects.finding import AssessmentFindingManager
from reporter.objects.output_file import AssessmentOutputFileManager
from reporter.objects.target import AssessmentTargetManager


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
        "users": AssessmentAssessmentUserManager,
    }


class AssessmentManager(RestManager, GetMixin, ListMixin, UpdateMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RestManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
