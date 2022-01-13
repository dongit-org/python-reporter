from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, ListMixin


class Finding(RESTObject):
    pass


class FindingManager(RESTManager, CreateMixin, ListMixin):
    _path = "findings"
    _obj_cls = Finding
