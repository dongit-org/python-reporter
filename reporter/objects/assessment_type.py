# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RESTManager, RESTObject
from reporter.mixins import GetMixin, ListMixin

__all__ = [
    "AssessmentType",
    "AssessmentTypeManager",
]


class AssessmentType(RESTObject):
    pass


class AssessmentTypeManager(RESTManager, GetMixin, ListMixin):
    _path = "assessment-types"
    _obj_cls = AssessmentType
