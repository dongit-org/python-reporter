# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin, UpdateMixin

__all__ = [
    "ToolTarget",
    "ToolTargetManager",
]


class ToolTarget(RestObject):
    pass


class ToolTargetManager(RestManager, ListMixin, UpdateMixin):
    _path = "tool-targets"
    _obj_cls = ToolTarget
