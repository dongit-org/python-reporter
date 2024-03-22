from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, UpdateMixin, DeleteMixin

__all__ = [
    "AssessmentComment",
    "AssessmentCommentManager",
    "AssessmentAssessmentCommentManager",
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
