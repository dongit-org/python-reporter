# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RESTManager, RESTObject
from reporter.mixins import (
    CRUDMixin,
    ListMixin,
    SearchMixin,
)

__all__ = [
    "FindingTemplate",
    "FindingTemplateManager",
]


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(
    RESTManager,
    CRUDMixin,
    ListMixin,
    SearchMixin,
):
    _path = "finding-templates"
    _obj_cls = FindingTemplate
