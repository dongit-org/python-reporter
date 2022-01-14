from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, ListMixin


class Client(RESTObject):
    pass


class ClientManager(RESTManager, CreateMixin, ListMixin):
    _path = "clients"
    _obj_cls = Client
