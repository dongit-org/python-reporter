# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import GetMixin, ListMixin

__all__ = [
    "AssessmentTemplate",
    "AssessmentTemplateManager",
]


class AssessmentTemplate(RestObject):
    pass


class AssessmentTemplateManager(RestManager, GetMixin, ListMixin):
    _path = "assessment-templates"
    _obj_cls = AssessmentTemplate
