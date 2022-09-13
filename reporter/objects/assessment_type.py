# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import GetMixin, ListMixin

__all__ = [
    "AssessmentType",
    "AssessmentTypeManager",
]


class AssessmentType(RestObject):
    pass


class AssessmentTypeManager(RestManager, GetMixin, ListMixin):
    _path = "assessment-types"
    _obj_cls = AssessmentType
