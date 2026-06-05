# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "FindingRetestCancelledEvent",
    "FindingRetestCancelledEventManager",
    "FindingRetestInquiryFindingRetestCancelledEventManager",
]


class FindingRetestCancelledEvent(RestObject):
    pass


class FindingRetestCancelledEventManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "finding-retest-cancelled-events"
    _obj_cls = FindingRetestCancelledEvent


class FindingRetestInquiryFindingRetestCancelledEventManager(RestManager, CreateMixin):
    _path = (
        "finding-retest-inquiries/{finding_retest_inquiry_id}"
        "/finding-retest-cancelled-events"
    )
    _parent_attrs = {"finding_retest_inquiry_id": "id"}
    _obj_cls = FindingRetestCancelledEvent
