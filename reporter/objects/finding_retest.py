# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "FindingRetest",
    "FindingRetestManager",
    "FindingFindingRetestManager",
]


class FindingRetest(RestObject):
    pass


class FindingRetestManager(RestManager, UpdateMixin, DeleteMixin):
    _path = "finding-retests"
    _obj_cls = FindingRetest


class FindingFindingRetestManager(RestManager, CreateMixin):
    _path = "findings/{finding_id}/finding-retests"
    _parent_attrs = {"finding_id": "id"}
    _obj_cls = FindingRetest
