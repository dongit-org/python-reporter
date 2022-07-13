from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin


class AssessmentUser(RESTObject):
    pass


class AssessmentAssessmentUserManager(
    RESTManager,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
):
    _path = "assessments/{assessment_id}/users"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = AssessmentUser
