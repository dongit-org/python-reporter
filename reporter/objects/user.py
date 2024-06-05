# pylint: disable = missing-module-docstring, missing-class-docstring

from typing import TYPE_CHECKING, Optional, List, Mapping
from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "User",
    "UserManager",
]


class User(RestObject):
    pass


class UserManager(RestManager, CreateMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "users"
    _obj_cls = User

    def me(
        self,
        include: Optional[List[str]] = None,
        query_data: Optional[Mapping[str, str]] = None,
        **kwargs,
    ) -> User:
        """Get the user who owns the API token

        Args:
            include: Related data to include in the response.
            query_data: Dict of additional query parameters
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The response from the server, serialized into the `User` type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """

        query_data = dict(query_data) if query_data else {}

        if include:
            query_data["include"] = ",".join(include)

        result = self.reporter.http_request(
            verb="get",
            path="users/me",
            query_data=query_data,
            **kwargs,
        )
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return User(self.reporter, result.json())
