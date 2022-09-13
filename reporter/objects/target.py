# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "Target",
    "TargetManager",
    "AssessmentTargetManager",
]


class Target(RestObject):
    pass


class TargetManager(RestManager, DeleteMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "targets"
    _obj_cls = Target


class AssessmentTargetManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/targets"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Target
