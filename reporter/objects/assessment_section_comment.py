# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "AssessmentSectionComment",
    "AssessmentSectionCommentManager",
    "AssessmentSectionAssessmentSectionCommentManager",
    "AssessmentSectionEventReplyManager",
]


class AssessmentSectionComment(RestObject):
    replies: "AssessmentSectionEventReplyManager"


class AssessmentSectionCommentManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "assessment-section-comments"
    _obj_cls = AssessmentSectionComment


class AssessmentSectionAssessmentSectionCommentManager(RestManager, CreateMixin):
    _path = "assessment-sections/{assessment_section_id}/assessment-section-comments"
    _parent_attrs = {"assessment_section_id": "id"}
    _obj_cls = AssessmentSectionComment


class AssessmentSectionEventReplyManager(RestManager, CreateMixin):
    _path = "assessment-section-events/{assessment_section_event_id}/assessment-section-comments"
    _parent_attrs = {"assessment_section_event_id": "id"}
    _obj_cls = AssessmentSectionComment
