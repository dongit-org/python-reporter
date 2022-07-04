from typing import Any, Dict

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin
from reporter.objects.target import AssessmentTargetManager


class Assessment(RESTObject):
    targets: AssessmentTargetManager

    def __init__(self, manager: RESTManager, attrs: Dict[str, Any]) -> None:
        super().__init__(manager, attrs)
        self.targets = AssessmentTargetManager(self.manager.reporter, parent=self)


class AssessmentManager(RESTManager, GetMixin, ListMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
