"""Wrapper for the Reporter API."""

from typing import Any, Dict, Optional

import requests

import reporter.exceptions


class Reporter(object):
    """Represents a Reporter server connection.

    Args:
        url: The URL of the Reporter server (defaults to https://reporter.dongit.nl)
        api_token: The user API token
    """

    api_token: str
    url: str

    session: requests.Session

    def __init__(
        self,
        api_token: str,
        url: Optional[str] = None,
    ) -> None:
        self.api_token = api_token
        self.url = url or "https://reporter.dongit.nl"

        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_token}"})

        # Delay import until now to avoid circular import errors
        import reporter.objects as objects

        self.assessments = objects.AssessmentManager(self)
        self.findings = objects.FindingManager(self)

    def http_request(
        self,
        verb: str,
        path: str,
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make an HTTP request to the Reporter server.

        Args:
            verb: The HTTP method to call ('get', 'post', 'put', 'delete')
            path: Path to query ('findings')
            query_data: Data to send as query string parameters
            post_data: Data to send in the body (will be converted to JSON)

        Returns:
            A requests Response object

        Raises:
            ReporterHttpError: When the return code is not 2xx
        """

        url = f"{self.url}/api/v1/{path}"

        result = self.session.request(
            method=verb,
            url=url,
            params=query_data,
            json=post_data,
            # Reporter returns with a redirect to /login if unauthorized.
            # TODO Remove this when fixed in Reporter.
            allow_redirects=False,
        )

        if 200 <= result.status_code < 300:
            return result

        raise reporter.exceptions.ReporterHttpError(
            error_message=result.content,
            response_code=result.status_code,
            response_body=result.content,
        )
