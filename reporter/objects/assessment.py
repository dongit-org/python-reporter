from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Assessment(RESTObject):
    pass


class AssessmentManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "assessments"
    _obj_cls = Assessment
