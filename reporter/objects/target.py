from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Target(RESTObject):
    pass


class TargetManager(RESTManager, GetMixin, ListMixin):
    _path = "targets"
    _obj_cls = Target


class AssessmentTargetManager(RESTManager, CreateMixin):
    _path = "assessments/{assessment_id}/targets"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Target
