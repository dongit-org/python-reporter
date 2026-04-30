# pylint: disable = missing-module-docstring, missing-class-docstring
from typing import Any, Mapping, Optional

from reporter.base import RestManager, RestObject
from reporter.mixins import CrudMixin, ListMixin
from .assessment import ClientAssessmentManager
from .team import ClientTeamManager
from .user import User

__all__ = [
    "Client",
    "ClientManager",
    "ClientAccountManagerManager",
    "ClientClientManagerManager",
]


class Client(RestObject):
    assessments: ClientAssessmentManager
    account_managers: "ClientAccountManagerManager"
    client_managers: "ClientClientManagerManager"
    teams: ClientTeamManager


class ClientManager(
    RestManager,
    CrudMixin,
    ListMixin,
):
    _path = "clients"
    _obj_cls = Client


class ClientAccountManagerManager(RestManager):
    _path = "clients/{client_id}/account-managers"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = User

    def assign(self, attrs: Mapping[str, Any], **kwargs: Any) -> None:
        """Assign a user as account manager to the parent client.

        Args:
            attrs: Attributes for the request. Must contain ``user_id``; may
                contain ``assign_to_future_assessments`` (boolean).
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        self.reporter.http_request(
            verb="post",
            path=self._path,
            post_data=attrs,
            **kwargs,
        )

    def remove(
        self,
        user_id: str,
        attrs: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Remove an account manager from the parent client.

        Args:
            user_id: The ID of the account manager to remove.
            attrs: Optional attributes for the request. May contain
                ``unassign_from_assessments`` (a list of assessment IDs).
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        self.reporter.http_request(
            verb="delete",
            path=f"{self._path}/{user_id}",
            post_data=attrs if attrs is not None else {},
            **kwargs,
        )


class ClientClientManagerManager(RestManager):
    _path = "clients/{client_id}/client-managers"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = User

    def update(self, attrs: Mapping[str, Any], **kwargs: Any) -> None:
        """Replace the list of client managers for the parent client.

        Args:
            attrs: Attributes for the request. Must contain ``client_managers``
                (a list of user IDs).
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        self.reporter.http_request(
            verb="put",
            path=self._path,
            post_data=attrs,
            **kwargs,
        )
