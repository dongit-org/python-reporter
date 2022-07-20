from reporter.base import RESTManager, RESTObject
from reporter.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    SearchMixin,
    UpdateMixin,
)

__all__ = [
    "FindingTemplate",
    "FindingTemplateManager",
]


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(
    RESTManager,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    SearchMixin,
    UpdateMixin,
):
    _path = "finding-templates"
    _obj_cls = FindingTemplate
