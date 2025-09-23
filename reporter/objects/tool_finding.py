# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import GetMixin, ListMixin, UpdateMixin

__all__ = [
    "ToolFinding",
    "ToolFindingManager",
]


class ToolFinding(RestObject):
    pass


class ToolFindingManager(RestManager, GetMixin, ListMixin, UpdateMixin):
    _path = "tool-findings"
    _obj_cls = ToolFinding
