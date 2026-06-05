# pylint: disable = missing-module-docstring, missing-class-docstring, duplicate-code

from typing import TYPE_CHECKING, Any, List, Mapping, Optional

from reporter.base import RestManager, RestObject
from reporter.mixins import DeleteMixin, GetMixin, ListMixin
from reporter.types import FileSpec

__all__ = [
    "ApiToken",
    "ApiTokenManager",
]


class ApiToken(RestObject):
    pass


class ApiTokenManager(RestManager, GetMixin, ListMixin, DeleteMixin):
    _path = "api-tokens"
    _obj_cls = ApiToken

    def create(
        self,
        attrs: Mapping[str, Any],
        file: Optional[FileSpec] = None,
        **kwargs: Any,
    ) -> ApiToken:
        """Create a new API token.

        The plaintext ``token`` is included once in the response and exposed as
        an attribute on the returned :class:`ApiToken`.

        Args:
            attrs: Attributes for the created object. Required: ``name``,
                ``abilities``. Optional: ``expires_at``, ``scope``, ``clients``,
                ``assessments``, ``user_id``.
            file: Unused; accepted for signature parity with
                :meth:`reporter.mixins.CreateMixin.create`.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The created :class:`ApiToken`, with the plaintext ``token`` attribute.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        files = {"file": file} if file is not None else None
        result = self.reporter.http_request(
            verb="post",
            path=self._path,
            post_data=attrs,
            files=files,
            **kwargs,
        )
        # Workaround for a Reporter bug: this endpoint returns the resource
        # wrapped in a ``data`` envelope rather than the flat shape every other
        # create endpoint (and the OpenAPI spec) uses. Revert this override
        # (and inherit ``CreateMixin``) once Reporter is fixed.
        body = result.json()
        return ApiToken(self.reporter, {**body["data"], "token": body["token"]})

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
