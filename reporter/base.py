from collections.abc import Sequence
from typing import Any, Dict, Iterable, List, Optional, Type

from reporter.client import Reporter


class RESTObject(object):
    """Represents an object built from server data.

    Args:
        attrs: Object attributes
    """

    reporter: Reporter

    _attrs: Dict[str, Any]
    _includes: Dict[str, Type["RESTObject"]] = {}
    _children: Dict[str, Type["RESTManager"]] = {}

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

    def __dir__(self) -> Iterable[str]:
        return set(self._attrs.keys()).union(super(RESTObject, self).__dir__())

    def __eq__(self, other: object):
        if not isinstance(other, RESTObject):
            return NotImplemented
        return self.id == other.id

    def __contains__(self, item: str):
        return item in self._attrs

    def _deserialize_includes(self):
        for include in self._includes:
            if include in self:
                if isinstance(self._attrs[include], List):
                    self._attrs[include] = [
                        self._includes[include](self.reporter, json_obj)
                        for json_obj in self._attrs[include]
                    ]
                    if include in self._children:
                        getattr(self, include)._list = self._attrs[include]
                else:
                    self._attrs[include] = self._includes[include](
                        self.reporter, self._attrs[include]
                    )


class RESTList(Sequence):
    """Represents a list of objects built from server data.

    Includes associated links and metadata.

    Args:
        data: List of RESTObject instances
        links: Dict of links (see Reporter API docs)
        meta: Dict of metadata (see Reporter API docs)
    """

    _data: List[RESTObject]
    links: Dict[str, str]
    meta: Dict[str, str]

    def __init__(
        self,
        data: List[RESTObject],
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


class RESTManager(Sequence):
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
    _obj_cls: Type[RESTObject]
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
