from reporter.base import RESTManager, RESTObject
from reporter.mixins import GetMixin, ListMixin, SearchMixin


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(RESTManager, GetMixin, ListMixin, SearchMixin):
    _path = "finding_templates"
    _obj_cls = FindingTemplate
