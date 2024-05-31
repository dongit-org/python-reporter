# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin

__all__ = [
    "Reaction",
    "ReactionManager",
]


class Reaction(RestObject):
    pass


# In the Reporter API, the Reaction resources's DELETE method behaves unexpectedly.
# Instead of DELETE reactions/{id}, it is DELETE reactions, and the model info is given as body
# parameters. This will be fixed in the next release, and when python-reporter is updated we should
# add the DeleteMixin to this manager.
class ReactionManager(RestManager, CreateMixin):
    _path = "reactions"
    _obj_cls = Reaction
