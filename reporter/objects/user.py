from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin


class User(RESTObject):
    pass


class UserManager(RESTManager, CreateMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "users"
    _obj_cls = User
