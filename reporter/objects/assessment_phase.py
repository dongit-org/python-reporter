from reporter.base import RESTManager, RESTObject
from reporter.mixins import UpdateMixin

__all__ = [
    "AssessmentPhase",
    "AssessmentPhaseManager",
]


class AssessmentPhase(RESTObject):
    pass


class AssessmentPhaseManager(RESTManager, UpdateMixin):
    _path = "assessment-phases"
    _obj_cls = AssessmentPhase
