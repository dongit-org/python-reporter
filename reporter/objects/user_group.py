from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin


class UserGroup(RESTObject):
    pass


class UserGroupManager(
    RESTManager,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "user-groups"
    _obj_cls = UserGroup


class ClientUserGroupManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/user-groups"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = UserGroup