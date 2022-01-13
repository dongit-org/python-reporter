from typing import Any, Dict, List, Optional

from reporter.client import Reporter


class Assessment(object):
    """Represents an assessment.

    Args:
        attrs: Assessment attributes
    """

    def __init__(self, attrs: Dict[str, Any]) -> None:
        self.attrs = attrs


class AssessmentManager(object):
    reporter: Reporter

    def __init__(self, reporter: Reporter) -> None:
        """AssessmentManager constructor

        Args:
            reporter: connection to use to make requests
        """
        self.reporter = reporter

    def list(self, filter: Optional[Dict[str, str]]) -> List[Assessment]:
        """Retrieve a list of assessments.

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
                                            path="assessments",
                                            query_data=query_data)

        return [
            Assessment(attrs=finding_data)
            for finding_data in result.json()["data"]
        ]
