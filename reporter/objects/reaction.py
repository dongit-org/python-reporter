# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin

__all__ = [
    "Reaction",
    "ReactionManager",
]


class Reaction(RestObject):
    pass


class ReactionManager(RestManager, CreateMixin, DeleteMixin):
    _path = "reactions"
    _obj_cls = Reaction
