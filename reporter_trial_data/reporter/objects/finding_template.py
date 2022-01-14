from reporter.base import RESTManager, RESTObject
from reporter.mixins import ListMixin


class FindingTemplate(RESTObject):
    pass


class FindingTemplateManager(RESTManager, ListMixin):
    _path = "finding_templates"
    _obj_cls = FindingTemplate
