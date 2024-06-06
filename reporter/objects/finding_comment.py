# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "FindingComment",
    "FindingCommentManager",
    "FindingFindingCommentManager",
    "FindingEventReplyManager",
]


class FindingComment(RestObject):
    replies: "FindingEventReplyManager"


class FindingCommentManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "finding-comments"
    _obj_cls = FindingComment


class FindingFindingCommentManager(RestManager, CreateMixin):
    _path = "findings/{finding_id}/finding-comments"
    _parent_attrs = {"finding_id": "id"}
    _obj_cls = FindingComment


class FindingEventReplyManager(RestManager, CreateMixin):
    _path = "finding-events/{finding_event_id}/finding-comments"
    _parent_attrs = {"finding_event_id": "id"}
    _obj_cls = FindingComment
