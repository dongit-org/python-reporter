from typing import Any, Dict, Iterable

from reporter.client import Reporter


class RESTObject(object):
    """Represents an object built from server data.

    Args:
        attrs: Object attributes
    """

    _attrs: Dict[str, Any]

    def __init__(self, attrs: Dict[str, Any]) -> None:
        self._attrs = attrs

    def __getattr__(self, attr: str) -> Any:
        try:
            return self._attrs[attr]
        except KeyError as exc:
            message = f"{type(self).__name__!r} object has no attribute '{attr}'"
            raise AttributeError(message) from exc

    def __dir__(self) -> Iterable[str]:
        return set(self._attrs.keys()).union(super(RESTObject, self).__dir__())


class RESTManager(object):
    """Base class for managers of RESTObjects."""

    reporter: Reporter

    def __init__(self, reporter: Reporter) -> None:
        """RESTManager constructor

        Args:
            reporter: connection to use to make requests
        """
        self.reporter = reporter
