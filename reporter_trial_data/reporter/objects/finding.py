from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Finding(RESTObject):
    pass


class FindingManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "findings"
    _obj_cls = Finding
