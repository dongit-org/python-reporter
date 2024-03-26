# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "FindingRetestInquiry",
    "FindingRetestInquiryManager",
    "FindingFindingRetestInquiryManager",
]


class FindingRetestInquiry(RestObject):
    pass


class FindingRetestInquiryManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "finding-retest-inquiries"
    _obj_cls = FindingRetestInquiry


class FindingFindingRetestInquiryManager(RestManager, CreateMixin):
    _path = "findings/{finding_id}/finding-retest-inquiries"
    _parent_attrs = {"finding_id": "id"}
    _obj_cls = FindingRetestInquiry
