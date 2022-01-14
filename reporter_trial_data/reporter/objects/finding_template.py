from reporter.base import RESTManager, RESTObject
from reporter.mixins import GetMixin, ListMixin


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(RESTManager, GetMixin, ListMixin):
    _path = "finding_templates"
    _obj_cls = FindingTemplate
