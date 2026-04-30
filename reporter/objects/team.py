# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, UpdateMixin
from .team_user import TeamTeamUserManager

__all__ = [
    "Team",
    "TeamManager",
    "ClientTeamManager",
]


class Team(RestObject):
    users: TeamTeamUserManager


class TeamManager(
    RestManager,
    DeleteMixin,
    UpdateMixin,
):
    _path = "teams"
    _obj_cls = Team


class ClientTeamManager(RestManager, CreateMixin):
    _path = "clients/{client_id}/teams"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Team
