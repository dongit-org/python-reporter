# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "Language",
    "LanguageManager",
]


class Language(RestObject):
    pass


class LanguageManager(RestManager, ListMixin):
    _path = "languages"
    _obj_cls = Language
