# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetRawMixin

__all__ = [
    "Document",
    "DocumentManager",
]


class Document(RestObject):
    pass


class DocumentManager(RestManager, DeleteMixin, CreateMixin, GetRawMixin):
    _path = "documents"
    _obj_cls = Document
