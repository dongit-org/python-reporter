from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.assessment import ClientAssessmentManager


class Client(RESTObject):
    _children = {
        "assessments": ClientAssessmentManager,
    }


class ClientManager(
    RESTManager,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "clients"
    _obj_cls = Client
