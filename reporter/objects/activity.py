from reporter.base import RESTManager, RESTObject
from reporter.mixins import ListMixin

__all__ = [
    "Activity",
    "ActivityManager",
]


class Activity(RESTObject):
    pass


class ActivityManager(RESTManager, ListMixin):
    _path = "activities"
    _obj_cls = Activity
