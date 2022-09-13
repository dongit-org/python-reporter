# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "AssessmentUser",
    "AssessmentAssessmentUserManager",
]


class AssessmentUser(RestObject):
    pass


class AssessmentAssessmentUserManager(
    RestManager,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
):
    _path = "assessments/{assessment_id}/users"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = AssessmentUser
