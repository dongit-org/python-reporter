# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import GetMixin, UpdateMixin

__all__ = [
    "TestCase",
    "TestCaseManager",
]


class TestCase(RestObject):
    pass


class TestCaseManager(RestManager, GetMixin, UpdateMixin):
    _path = "test-cases"
    _obj_cls = TestCase
