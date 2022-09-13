# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import UpdateMixin

__all__ = [
    "AssessmentSection",
    "AssessmentSectionManager",
]


class AssessmentSection(RestObject):
    pass


class AssessmentSectionManager(RestManager, UpdateMixin):
    _path = "assessment-sections"
    _obj_cls = AssessmentSection
