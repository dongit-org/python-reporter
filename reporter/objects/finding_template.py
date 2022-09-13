# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import (
    CRUDMixin,
    ListMixin,
    SearchMixin,
)

__all__ = [
    "FindingTemplate",
    "FindingTemplateManager",
]


class FindingTemplate(RestObject):
    pass


class FindingTemplateManager(
    RestManager,
    CRUDMixin,
    ListMixin,
    SearchMixin,
):
    _path = "finding-templates"
    _obj_cls = FindingTemplate
