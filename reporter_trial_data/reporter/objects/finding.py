from typing import Any, Dict, List, Optional

from reporter.client import Reporter


class Finding(object):
    """Represents a finding.

    Args:
        attrs: Finding attributes
    """

    def __init__(self, attrs: Dict[str, Any]) -> None:
        self.attrs = attrs


class FindingManager(object):
    reporter: Reporter

    def __init__(self, reporter: Reporter) -> None:
        """FindingManager constructor

        Args:
            reporter: connection to use to make requests
        """
        self.reporter = reporter

    def list(self, filter: Optional[Dict[str, str]] = None) -> List[Finding]:
        """Retrieve a list of findings.

        Args:
            kwargs: query string parameters for HTTP request
        """
        if filter is not None:
            query_data = {
                f"filter[{key}]": value
                for (key, value) in filter.items()
            }
        else:
            query_data = {}

        result = self.reporter.http_request(verb="get",
                                            path="findings",
                                            query_data=query_data)

        return [
            Finding(attrs=finding_data)
            for finding_data in result.json()["data"]
        ]
