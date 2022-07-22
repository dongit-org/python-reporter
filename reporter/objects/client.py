# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CRUDMixin, ListMixin
from reporter.objects.assessment import ClientAssessmentManager
from reporter.objects.user_group import ClientUserGroupManager

__all__ = [
    "Client",
    "ClientManager",
]


class Client(RESTObject):
    _children = {
        "assessments": ClientAssessmentManager,
        "user_groups": ClientUserGroupManager,
    }


class ClientManager(
    RESTManager,
    CRUDMixin,
    ListMixin,
):
    _path = "clients"
    _obj_cls = Client
