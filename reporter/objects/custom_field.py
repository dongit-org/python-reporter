# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "CustomField",
    "CustomFieldManager",
]


class CustomField(RestObject):
    pass


class CustomFieldManager(RestManager, ListMixin):
    _path = "custom-fields"
    _obj_cls = CustomField
