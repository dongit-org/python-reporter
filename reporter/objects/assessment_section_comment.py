# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "AssessmentSectionComment",
    "AssessmentSectionCommentManager",
    "AssessmentSectionAssessmentSectionCommentManager",
]


class AssessmentSectionComment(RestObject):
    pass


class AssessmentSectionCommentManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "assessment-section-comments"
    _obj_cls = AssessmentSectionComment


class AssessmentSectionAssessmentSectionCommentManager(RestManager, CreateMixin):
    _path = "assessment-sections/{assessment_section_id}/assessment-section-comments"
    _parent_attrs = {"assessment_section_id": "id"}
    _obj_cls = AssessmentSectionComment
