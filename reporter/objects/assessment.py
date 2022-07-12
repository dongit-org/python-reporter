from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.finding import AssessmentFindingManager
from reporter.objects.target import AssessmentTargetManager


class Assessment(RESTObject):
    _children = {
        "findings": AssessmentFindingManager,
        "targets": AssessmentTargetManager,
    }


class AssessmentManager(RESTManager, GetMixin, ListMixin, UpdateMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
