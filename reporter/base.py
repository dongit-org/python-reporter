"""Base classes for API models.

This module contains base classes that should be inherited by objects
representing API models, managers of these objects, and lists of these objects.

"""

from collections.abc import Mapping, Sequence
from typing import Any, Dict, Generic, Iterable, List, Optional, Type, TypeVar

from reporter.client import Reporter

__all__ = [
    "RESTObject",
    "RESTList",
    "RESTManager",
]


class RESTObject(Mapping):
    """Represents an object built from server data.

    Args:
        attrs: Object attributes
    """

    reporter: Reporter

    _attrs: Dict[str, Any]
    _includes: Dict[str, Type["RESTObject"]] = {}
    _children: Dict[str, Type["RESTManager"]] = {}

    def __init__(self, reporter: Reporter, attrs: Dict[str, Any]) -> None:
        """
        Args:
            reporter: The :class:`~reporter.Reporter` instance used by this object to
                perform requests.
            attrs: The attributes to assign to this object.

        """
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
        if isinstance(val, RESTObject):
            return dict(self._attrs[attr])
        if isinstance(val, list) and len(val) > 0 and isinstance(val[0], RESTObject):
            # We assume that either all elements of val are RESTObjects or none
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
        if not isinstance(other, RESTObject):
            return NotImplemented
        return self.id == other.id

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


O = TypeVar("O", bound=RESTObject)


class RESTList(Sequence, Generic[O]):
    """Represents a list of objects built from server data.

    Includes associated links and metadata.

    Args:
        data: List of RESTObject instances
        links: Dict of links (see Reporter API docs)
        meta: Dict of metadata (see Reporter API docs)
    """

    _data: List[O]
    links: Dict[str, str]
    meta: Dict[str, str]

    def __init__(
        self,
        data: List[O],
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


class RESTManager(Sequence, Generic[O]):
    """Base class for managers of RESTObjects."""

    reporter: Reporter

    _parent: Optional[RESTObject]
    _parent_attrs: Dict[str, str]
    _path: str
    _computed_path: str

    # We need to consider the case that an instance of this class is assigned
    # to an attribute of an instance `r` of RESTObject with the same name as a
    # key in `r._includes`. This occurs e.g. for
    # `Assessment._children["targets"]`. Hence we make RESTManager derive
    # collections.abc.Sequence and implement the required methods, so that this
    # class exposes a convenient API for the included list. We assume that this
    # can only happen if this class is assigned to an attribute of `r` that is
    # a plural noun (e.g. "targets" instead of "target").
    _obj_cls: Type[O]
    _list: List[RESTObject] = []

    def __init__(
        self,
        reporter: Reporter,
        parent: Optional[RESTObject] = None,
    ) -> None:
        """RESTManager constructor

        Args:
            reporter: connection to use to make requests
            parent: RESTObject to which the manager is attached, if applicable
        """
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
