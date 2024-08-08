"""Module containing additional helper types

"""

from typing import List, Type, Mapping, Any, TypeVar, Generic, TYPE_CHECKING
from reporter.client import Reporter

if TYPE_CHECKING:
    from .base import RestObject

__all__ = [
    "Polymorphic",
]

T = TypeVar("T", bound="RestObject")


class Polymorphic(Generic[T]):
    """Used for includes that can have multiple types.

    Example:
    ```
    cls = Polymorphic([ModelTypeA, ModelTypeB, ModelTypeC])
    cls(rc, {"type": "ModelTypeB", ...})
    ```
    returns an instance of ModelTypeB.
    """

    _types: List[Type[T]]
    _key: str

    def __init__(self, types: List[Type[T]], key: str):
        self._types = types
        self._key = key

    def _get_class(self, class_name: str) -> Type[T]:
        return next(t for t in self._types if t.__name__ == class_name)

    def __call__(self, reporter: Reporter, attrs: Mapping[str, Any]) -> T:
        class_name = attrs[self._key]
        cls = self._get_class(class_name)
        return cls(reporter, attrs)
