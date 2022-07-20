from reporter.base import RESTManager, RESTObject
from reporter.mixins import UpdateMixin

__all__ = [
    "AssessmentSection",
    "AssessmentSectionManager",
]


class AssessmentSection(RESTObject):
    pass


class AssessmentSectionManager(RESTManager, UpdateMixin):
    _path = "assessment-sections"
    _obj_cls = AssessmentSection
