# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import ListMixin

__all__ = [
    "Role",
    "GlobalRoleManager",
    "AssessmentRoleManager",
]


class Role(RestObject):
    pass


class GlobalRoleManager(RestManager, ListMixin):
    _path = "roles"
    _obj_cls = Role


class AssessmentRoleManager(RestManager, ListMixin):
    _path = "assessment-roles"
    _obj_cls = Role
