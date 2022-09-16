"""This module contains exceptions raised by this library."""

from typing import Optional, Union

__all__ = [
    "ReporterError",
    "ReporterHttpError",
]


class ReporterError(Exception):
    """Base class for Reporter errors.

    Args:
       error_message: The error message.
       response_code: The response code returned by the server.
       response_body: The response body returned by the server.

    """

    def __init__(
        self,
        error_message: Union[bytes, str] = "",
        response_code: Optional[int] = None,
        response_body: Optional[bytes] = None,
    ) -> None:
        Exception.__init__(self, error_message)

        if isinstance(error_message, bytes):
            self.error_message = error_message.decode()
        else:
            self.error_message = error_message

        self.response_code = response_code
        self.response_body = response_body

    def __str__(self) -> str:
        if self.response_code is not None:
            return f"{self.response_code}: {self.error_message}"
        return f"{self.error_message}"


class ReporterHttpError(ReporterError):
    """Raised on unsuccessful HTTP response."""
