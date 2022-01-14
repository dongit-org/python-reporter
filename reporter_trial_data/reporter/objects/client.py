from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Client(RESTObject):
    pass


class ClientManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "clients"
    _obj_cls = Client
