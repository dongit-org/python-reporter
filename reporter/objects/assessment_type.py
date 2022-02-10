from reporter.base import RESTManager, RESTObject
from reporter.mixins import GetMixin, ListMixin


class AssessmentType(RESTObject):
    pass


class AssessmentTypeManager(RESTManager, GetMixin, ListMixin):
    _path = "assessment_types"
    _obj_cls = AssessmentType
