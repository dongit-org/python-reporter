"""Base classes for API models.

This module contains base classes that should be inherited by objects
representing API models, managers of these objects, and lists of these objects.

"""

from collections.abc import Sequence
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from reporter.client import Reporter

__all__ = [
    "RestObject",
    "RestList",
    "RestManager",
]


class RestObject:
    """Represents an object built from server data.

    Args:
        reporter: The :class:`~reporter.Reporter` instance used by this object to
            perform requests.
        attrs: Object attributes
    """

    reporter: Reporter

    _attrs: Dict[str, Any]
    _includes: Dict[str, Type["RestObject"]] = {}
    _children: Dict[str, Type["RestManager"]] = {}

    def __init__(self, reporter: Reporter, attrs: Dict[str, Any]) -> None:
        self.reporter = reporter
        self._attrs = attrs
        for key, mgr_cls in self._children.items():
            setattr(self, key, mgr_cls(self.reporter, parent=self))
        self._deserialize_includes()

    def __getattr__(self, attr: str) -> Any:
        try:
            return self._attrs[attr]
        except KeyError as exc:
            message = f"{type(self).__name__!r} object has no attribute '{attr}'"
            raise AttributeError(message) from exc

    def __getitem__(self, attr: str) -> Any:
        val = self._attrs[attr]
        if isinstance(val, RestObject):
            return dict(self._attrs[attr])
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], RestObject):
            # We assume that either all elements of val are RestObjects or none
            # of them are.
            return [dict(v) for v in val]
        return val

    def __iter__(self) -> Any:
        return iter(self._attrs)

    def __len__(self) -> int:
        return len(self._attrs)

    def __dir__(self) -> Iterable[str]:
        return set(self._attrs.keys()).union(super().__dir__())

    def __eq__(self, other: object):
        if not isinstance(other, RestObject):
            return NotImplemented
        return self.id == other.id

    # This is to ensure that the dict() function can accept this class.
    # See https://stackoverflow.com/a/40667249
    def keys(self):  # pylint: disable = missing-function-docstring
        return self._attrs.keys()

    def _deserialize_includes(self):
        for include, cls in self._includes.items():
            if include not in self:
                continue

            if isinstance(self._attrs[include], List):
                self._attrs[include] = [
                    cls(self.reporter, json_obj) for json_obj in self._attrs[include]
                ]
                if include in self._children:
                    getattr(  # pylint: disable = protected-access
                        self, include
                    )._list = self._attrs[include]
            else:
                self._attrs[include] = cls(self.reporter, self._attrs[include])


ChildOfRestObject = TypeVar("ChildOfRestObject", bound=RestObject)


class RestList(Sequence, Generic[ChildOfRestObject]):
    """Represents a list of :class:`~reporter.base.RestObject` instances built from server data.

    Includes associated links and metadata.

    Args:
        data: List of :class:`~reporter.base.RestObject` instances
        links: Dict of links (see Reporter API docs)
        meta: Dict of metadata (see Reporter API docs)
    """

    _data: List[ChildOfRestObject]
    links: Dict[str, str]
    meta: Dict[str, str]

    def __init__(
        self,
        data: List[ChildOfRestObject],
        links: Dict[str, str],
        meta: Dict[str, str],
    ) -> None:
        self._data = data
        self.links = links
        self.meta = meta

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class RestManager(Sequence, Generic[ChildOfRestObject]):
    """Base class for :class:`~reporter.base.RestObject` managers.

    Args:
        reporter: connection to use to make requests
        parent: :class:`~reporter.base.RestObject` to which the manager is attached, if applicable
    """

    reporter: Reporter

    _parent: Optional[RestObject]
    _parent_attrs: Dict[str, str]
    _path: str
    _computed_path: str

    # We need to consider the case that an instance of this class is assigned
    # to an attribute of an instance `r` of RestObject with the same name as a
    # key in `r._includes`. This occurs e.g. for
    # `Assessment._children["targets"]`. Hence we make RestManager derive
    # collections.abc.Sequence and implement the required methods, so that this
    # class exposes a convenient API for the included list. We assume that this
    # can only happen if this class is assigned to an attribute of `r` that is
    # a plural noun (e.g. "targets" instead of "target").
    #
    # For example client.assessments refers to both the assessments manager and
    # a retrieved list of assessments, and can be used in both ways.
    _obj_cls: Type[ChildOfRestObject]
    _list: List[RestObject] = []

    def __init__(
        self,
        reporter: Reporter,
        parent: Optional[RestObject] = None,
    ) -> None:
        self.reporter = reporter
        self._parent = parent
        self._path = self._compute_path()

    def __getitem__(self, index):
        return self._list[index]

    def __len__(self):
        return len(self._list)

    def _compute_path(self) -> str:
        if self._parent is None:
            return self._path

        data = {
            pair[0]: getattr(self._parent, pair[1])
            for pair in self._parent_attrs.items()
        }
        return self._path.format(**data)
