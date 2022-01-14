from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Target(RESTObject):
    pass


class TargetManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "targets"
    _obj_cls = Target
