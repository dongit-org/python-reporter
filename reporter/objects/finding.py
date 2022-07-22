# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "Finding",
    "FindingManager",
    "AssessmentFindingManager",
]


class Finding(RESTObject):
    pass


class FindingManager(RESTManager, DeleteMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "findings"
    _obj_cls = Finding


class AssessmentFindingManager(RESTManager, CreateMixin):
    _path = "assessments/{assessment_id}/findings"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Finding
