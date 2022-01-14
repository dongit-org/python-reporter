from typing import Any, Dict

from reporter.client import Reporter


class RESTObject(object):
    """Represents an object built from server data.

    Args:
        attrs: Object attributes
    """

    def __init__(self, attrs: Dict[str, Any]) -> None:
        self.attrs = attrs


class RESTManager(object):
    """Base class for managers of RESTObjects."""

    reporter: Reporter

    def __init__(self, reporter: Reporter) -> None:
        """RESTManager constructor

        Args:
            reporter: connection to use to make requests
        """
        self.reporter = reporter
