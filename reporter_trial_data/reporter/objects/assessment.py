from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, ListMixin


class Assessment(RESTObject):
    pass


class AssessmentManager(RESTManager, CreateMixin, ListMixin):
    _path = "assessments"
    _obj_cls = Assessment
