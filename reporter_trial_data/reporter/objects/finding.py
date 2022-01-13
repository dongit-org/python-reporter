from reporter.base import RESTManager, RESTObject
from reporter.mixins import ListMixin


class Finding(RESTObject):
    pass


class FindingManager(RESTManager, ListMixin):
    _path = "findings"
    _obj_cls = Finding
