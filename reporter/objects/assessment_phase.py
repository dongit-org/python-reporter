# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import UpdateMixin

__all__ = [
    "AssessmentPhase",
    "AssessmentPhaseManager",
]


class AssessmentPhase(RestObject):
    pass


class AssessmentPhaseManager(RestManager, UpdateMixin):
    _path = "assessment-phases"
    _obj_cls = AssessmentPhase
