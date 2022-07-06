from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, SearchMixin, UpdateMixin


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(
    RESTManager, CreateMixin, GetMixin, ListMixin, SearchMixin, UpdateMixin
):
    _path = "finding-templates"
    _obj_cls = FindingTemplate
