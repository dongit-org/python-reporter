from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin, GetRawMixin


class Document(RESTObject):
    pass


class DocumentManager(RESTManager, DeleteMixin, CreateMixin, GetRawMixin):
    _path = "documents"
    _obj_cls = Document
