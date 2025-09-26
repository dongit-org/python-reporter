# pylint: disable = missing-module-docstring, missing-class-docstring
from typing import TYPE_CHECKING, Mapping, Any

from reporter.base import RestManager, RestObject
from reporter.helpers import Polymorphic
from reporter.mixins import ListMixin
from .finding_created_event import FindingCreatedEvent
from .finding_review_event import FindingReviewEvent
from .finding_published_event import FindingPublishedEvent
from .finding_comment import FindingComment
from .finding_retest_inquiry import FindingRetestInquiry
from .finding_retest import FindingRetest
from .finding_retest_cancelled_event import FindingRetestCancelledEvent
from .finding_status_change import FindingStatusChange
from .finding_import_event import FindingImportEvent
from .finding_resolver_event import FindingResolverEvent

if TYPE_CHECKING:
    from reporter import Reporter

__all__ = [
    "FindingEvent",
    "FindingEventManager",
]


FindingEvent = Polymorphic(
    [
        FindingCreatedEvent,
        FindingReviewEvent,
        FindingPublishedEvent,
        FindingComment,
        FindingRetestInquiry,
        FindingRetest,
        FindingRetestCancelledEvent,
        FindingStatusChange,
        FindingImportEvent,
        FindingResolverEvent,
    ],
    "finding_event_type",
)


class FindingEventManager(RestManager, ListMixin):
    _path = "finding-events"
    _obj_cls = RestObject

    def _obj_cast(self, reporter: "Reporter", event: Mapping[str, Any]) -> RestObject:
        return FindingEvent(reporter, event)
