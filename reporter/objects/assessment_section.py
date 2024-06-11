# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import GetMixin, UpdateMixin
from .assessment_section_comment import AssessmentSectionAssessmentSectionCommentManager

__all__ = [
    "AssessmentSection",
    "AssessmentSectionManager",
]


class AssessmentSection(RestObject):
    comments: AssessmentSectionAssessmentSectionCommentManager


class AssessmentSectionManager(RestManager, GetMixin, UpdateMixin):
    _path = "assessment-sections"
    _obj_cls = AssessmentSection
