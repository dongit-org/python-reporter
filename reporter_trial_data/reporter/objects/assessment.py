from reporter.base import RESTManager, RESTObject
from reporter.mixins import ListMixin


class Assessment(RESTObject):
    pass


class AssessmentManager(RESTManager, ListMixin):
    _path = "assessments"
    _obj_cls = Assessment
