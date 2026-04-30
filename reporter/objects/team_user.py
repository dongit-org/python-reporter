# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin

__all__ = [
    "TeamUser",
    "TeamTeamUserManager",
]


class TeamUser(RestObject):
    pass


class TeamTeamUserManager(
    RestManager,
    CreateMixin,
    UpdateMixin,
    DeleteMixin,
):
    _path = "teams/{team_id}/users"
    _parent_attrs = {"team_id": "id"}
    _obj_cls = TeamUser
