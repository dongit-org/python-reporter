from typing import Any, Dict, List, Optional

from reporter.base import RESTList, RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin
from reporter.objects.assessment_phase import AssessmentPhase
from reporter.objects.finding import AssessmentFindingManager
from reporter.objects.target import AssessmentTargetManager


class Assessment(RESTObject):
    findings: AssessmentFindingManager
    targets: AssessmentTargetManager

    def __init__(self, manager: RESTManager, attrs: Dict[str, Any]) -> None:
        super().__init__(manager, attrs)
        self.findings = AssessmentFindingManager(self.manager.reporter, parent=self)
        self.targets = AssessmentTargetManager(self.manager.reporter, parent=self)


class AssessmentManager(RESTManager, GetMixin, ListMixin, UpdateMixin):
    _path = "assessments"
    _obj_cls = Assessment

    def get(
        self,
        id: str,
        includes: List[str] = [],
    ) -> RESTObject:
        assessment = super().get(id, includes)
        if "phases" in assessment:
            setattr(
                assessment,
                "phases",
                [AssessmentPhase(self, phase) for phase in assessment.phases],
            )
        return assessment

    def list(
        self,
        filter: Dict[str, str] = {},
        sorts: List[str] = [],
        includes: List[str] = [],
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> RESTList:
        assessments = super().list(filter, sorts, includes, page, page_size)
        for assessment in assessments:
            if "phases" in assessment:
                setattr(
                    assessment,
                    "phases",
                    [AssessmentPhase(self, phase) for phase in assessment.phases],
                )
        return assessments


class ClientAssessmentManager(RESTManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
