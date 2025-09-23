# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "FindingLayout",
    "FindingLayoutManager",
]


class FindingLayout(RestObject):
    pass


class FindingLayoutManager(RestManager, ListMixin):
    _path = "finding-layouts"
    _obj_cls = FindingLayout
