# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "User",
    "UserManager",
]


class User(RestObject):
    pass


class UserManager(RestManager, CreateMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "users"
    _obj_cls = User
