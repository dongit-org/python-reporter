from reporter.base import RESTManager, RESTObject
from reporter.mixins import ListMixin


class Role(RESTObject):
    pass


class GlobalRoleManager(RESTManager, ListMixin):
    _path = "roles"
    _obj_cls = Role


class AssessmentRoleManager(RESTManager, ListMixin):
    _path = "assessment-roles"
    _obj_cls = Role
