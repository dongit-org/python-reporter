# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CrudMixin, ListMixin

__all__ = [
    "Client",
    "ClientManager",
]


class Client(RestObject):
    pass


class ClientManager(
    RestManager,
    CrudMixin,
    ListMixin,
):
    _path = "clients"
    _obj_cls = Client
