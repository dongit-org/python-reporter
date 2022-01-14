from typing import Optional, Union


class ReporterError(Exception):

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
        else:
            return f"{self.error_message}"


class ReporterHttpError(ReporterError):
    pass
