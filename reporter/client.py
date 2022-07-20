from typing import Any, Dict, Optional

import requests

import reporter.exceptions


__all__ = [
    "Reporter",
]


class Reporter(object):
    """Represents a Reporter server connection.

    Attributes:
        api_token: The Reporter API token to use for authentication.
        session: the ``requests.Session`` object used to make HTTP requests.
        ssl_verify: Whether to verify the server's SSL certificate.
        url: The URL of the Reporter server.

    """

    api_token: str
    ssl_verify: bool
    url: str

    session: requests.Session

    def __init__(
        self,
        api_token: str,
        ssl_verify: bool = True,
        url: str = "https://reporter.dongit.nl",
    ) -> None:
        """Initialize the Reporter instance.

        Args:
            api_token: The Reporter API token to use for authentication.
            ssl_verify: Whether to verify the server's SSL certificate.
            url: The URL of the Reporter server.

        """
        self.api_token = api_token
        self.ssl_verify = ssl_verify
        self.url = url

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Authorization": f"Bearer {api_token}",
            }
        )

        # Delay import until now to avoid circular import errors
        import reporter.objects as objects

        self.activities = objects.ActivityManager(self)
        self.assessments = objects.AssessmentManager(self)
        self.assessment_phases = objects.AssessmentPhaseManager(self)
        self.assessment_sections = objects.AssessmentSectionManager(self)
        self.assessment_types = objects.AssessmentTypeManager(self)
        self.clients = objects.ClientManager(self)
        self.documents = objects.DocumentManager(self)
        self.findings = objects.FindingManager(self)
        self.finding_templates = objects.FindingTemplateManager(self)
        self.output_files = objects.OutputFileManager(self)
        self.targets = objects.TargetManager(self)
        self.user_groups = objects.UserGroupManager(self)
        self.users = objects.UserManager(self)

    def http_request(
        self,
        verb: str,
        path: str,
        headers: Dict[str, str] = {},
        query_data: Optional[Dict[str, Any]] = None,
        post_data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """Make an HTTP request to the Reporter server.

        Args:
            verb: The HTTP method to call (e.g. ``get``, ``post``, ``put``, ``delete``).
            path: Path to query (e.g. ``findings/1`` for ``/api/v1/findings/1``).
            headers: Extra HTTP headers; will overwrite default headers.
            query_data: Data to send as query string parameters.
            post_data: Data to send in the body. This will be converted to JSON unless
                ``files`` is not ``None``.
            files: The files to send in the request. If this is not ``None``, then the
                request will be a ``multipart/form-data`` request.

        Returns:
            A requests Response object corresponding to the response from the Reporter
            server.

        Raises:
            ReporterHttpError: If the return code is not 2xx.
        """

        url = f"{self.url}/api/v1/{path}"

        # If files is present, we don't sent JSON.
        if files is not None:
            data = post_data
            json = None
        else:
            data = None
            json = post_data

        result = self.session.request(
            method=verb,
            url=url,
            headers=headers,
            params=query_data,
            data=data,
            json=json,
            files=files,
            verify=self.ssl_verify,
        )

        if 200 <= result.status_code < 300:
            return result

        raise reporter.exceptions.ReporterHttpError(
            error_message=result.content,
            response_code=result.status_code,
            response_body=result.content,
        )
