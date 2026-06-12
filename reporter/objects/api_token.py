# pylint: disable = missing-module-docstring, missing-class-docstring, duplicate-code

from typing import TYPE_CHECKING, Any, List, Mapping, Optional

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin

__all__ = [
    "ApiToken",
    "ApiTokenManager",
]


class ApiToken(RestObject):
    pass


class ApiTokenManager(RestManager, CreateMixin, GetMixin, ListMixin, DeleteMixin):
    _path = "api-tokens"
    _obj_cls = ApiToken

    # ``create`` is inherited from :class:`CreateMixin`. The endpoint returns
    # the created resource as a flat JSON object (as of Reporter 2026.06.30),
    # including the plaintext ``token`` field, which is therefore exposed as an
    # attribute on the returned :class:`ApiToken`.

    def me(
        self,
        include: Optional[str | List[str]] = None,
        query_data: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> ApiToken:
        """Get the API token used to authenticate the current request.

        Args:
            include: Related data to include in the response.
            query_data: Dict of additional query parameters
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The response from the server, serialized into the `ApiToken` type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        query_data = dict(query_data) if query_data else {}

        if include:
            query_data["include"] = include

        result = self.reporter.http_request(
            verb="get",
            path="api-tokens/me",
            query_data=query_data,
            **kwargs,
        )
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return ApiToken(self.reporter, result.json())
