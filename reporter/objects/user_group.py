# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "UserGroup",
    "UserGroupManager",
    "ClientUserGroupManager",
]


class UserGroup(RestObject):
    pass


class UserGroupManager(
    RestManager,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "user-groups"
    _obj_cls = UserGroup


class ClientUserGroupManager(RestManager, CreateMixin):
    _path = "clients/{client_id}/user-groups"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = UserGroup
