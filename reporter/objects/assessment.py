from typing import Any, Dict

from reporter.base import RESTManager, RESTObject
from reporter.client import Reporter
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.finding import AssessmentFindingManager
from reporter.objects.target import AssessmentTargetManager


class Assessment(RESTObject):
    findings: AssessmentFindingManager
    targets: AssessmentTargetManager

    def __init__(self, reporter: Reporter, attrs: Dict[str, Any]) -> None:
        super().__init__(reporter, attrs)
        self.findings = AssessmentFindingManager(self.reporter, parent=self)
        self.targets = AssessmentTargetManager(self.reporter, parent=self)


class AssessmentManager(RESTManager, GetMixin, ListMixin, UpdateMixin):
    _path = "assessments"
    _obj_cls = Assessment


class ClientAssessmentManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
