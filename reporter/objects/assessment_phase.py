from reporter.base import RESTManager, RESTObject
from reporter.mixins import UpdateMixin


class AssessmentPhase(RESTObject):
    pass


class AssessmentPhaseManager(RESTManager, UpdateMixin):
    _path = "assessment-phases"
    _obj_cls = AssessmentPhase
