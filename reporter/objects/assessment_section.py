from reporter.base import RESTManager, RESTObject
from reporter.mixins import UpdateMixin


class AssessmentSection(RESTObject):
    pass


class AssessmentPhaseManager(RESTManager, UpdateMixin):
    _path = "assessment-sections"
    _obj_cls = AssessmentSection
