from typing import Any, Dict

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin
from reporter.objects.assessment import ClientAssessmentManager


class Client(RESTObject):
    assessments: ClientAssessmentManager

    def __init__(self, manager: RESTManager, attrs: Dict[str, Any]) -> None:
        super().__init__(manager, attrs)
        self.assessments = ClientAssessmentManager(self.manager.reporter, parent=self)


class ClientManager(RESTManager, CreateMixin, GetMixin, ListMixin):
    _path = "clients"
    _obj_cls = Client
