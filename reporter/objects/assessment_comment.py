# pylint: disable = missing-module-docstring, missing-class-docstring, redefined-builtin

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, UpdateMixin, DeleteMixin

__all__ = [
    "AssessmentComment",
    "AssessmentCommentManager",
    "AssessmentAssessmentCommentManager",
    "AssessmentCommentReplyManager",
]


class AssessmentComment(RestObject):
    pass


class AssessmentCommentManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "assessment-comments"
    _obj_cls = AssessmentComment


class AssessmentAssessmentCommentManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/assessment-comments"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = AssessmentComment


class AssessmentCommentReplyManager(RestManager, CreateMixin):
    _path = "assessment-events/{assessment_event_id}/assessment-comments"
    _parent_attrs = {"assessment_event_id": "id"}
    _obj_cls = AssessmentComment
