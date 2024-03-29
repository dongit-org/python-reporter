# pylint: disable = missing-module-docstring, missing-class-docstring
from reporter.base import RestManager
from reporter.mixins import CreateMixin
from reporter.objects.finding_comment import FindingComment

__all__ = [
    "FindingEventReplyManager",
]


class FindingEventReplyManager(RestManager, CreateMixin):
    _path = "finding-events/{finding_event_id}/finding-comments"
    _parent_attrs = {"finding_event_id": "id"}
    _obj_cls = FindingComment
