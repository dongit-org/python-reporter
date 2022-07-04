from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Assessment(RESTObject):
    pass


class AssessmentManager(RESTManager, GetMixin, ListMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
