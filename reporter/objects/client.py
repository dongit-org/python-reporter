from typing import Any, Dict

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.assessment import ClientAssessmentManager


class Client(RESTObject):
    assessments: ClientAssessmentManager

    def __init__(self, manager: RESTManager, attrs: Dict[str, Any]) -> None:
        super().__init__(manager, attrs)
        self.assessments = ClientAssessmentManager(self.manager.reporter, parent=self)


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
