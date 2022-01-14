from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class User(RESTObject):
    pass


class UserManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "users"
    _obj_cls = User
