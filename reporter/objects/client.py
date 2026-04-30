# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CrudMixin, ListMixin
from .assessment import ClientAssessmentManager
from .team import ClientTeamManager

__all__ = [
    "Client",
    "ClientManager",
]


class Client(RestObject):
    assessments: ClientAssessmentManager
    teams: ClientTeamManager


class ClientManager(
    RestManager,
    CrudMixin,
    ListMixin,
):
    _path = "clients"
    _obj_cls = Client
