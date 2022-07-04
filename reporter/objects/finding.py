from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin


class Finding(RESTObject):
    pass


class FindingManager(RESTManager, GetMixin, ListMixin):
    _path = "findings"
    _obj_cls = Finding


class AssessmentFindingManager(RESTManager, CreateMixin):
    _path = "assessments/{assessment_id}/findings"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Finding
