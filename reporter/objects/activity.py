# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "Activity",
    "ActivityManager",
]


class Activity(RestObject):
    pass


class ActivityManager(RestManager, ListMixin):
    _path = "activities"
    _obj_cls = Activity
