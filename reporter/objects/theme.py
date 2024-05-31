# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "Theme",
    "ThemeManager",
]


class Theme(RestObject):
    pass


class ThemeManager(RestManager, ListMixin):
    _path = "themes"
    _obj_cls = Theme
