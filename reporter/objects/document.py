from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, GetRawMixin


class Document(RESTObject):
    pass


class DocumentManager(RESTManager, CreateMixin, GetRawMixin):
    _path = "documents"
    _obj_cls = Document
