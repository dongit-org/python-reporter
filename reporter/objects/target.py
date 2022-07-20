from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "Target",
    "TargetManager",
    "AssessmentTargetManager",
]


class Target(RESTObject):
    pass


class TargetManager(RESTManager, DeleteMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "targets"
    _obj_cls = Target


class AssessmentTargetManager(RESTManager, CreateMixin):
    _path = "assessments/{assessment_id}/targets"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Target
