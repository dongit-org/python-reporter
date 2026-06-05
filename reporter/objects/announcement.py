# pylint: disable = missing-module-docstring, missing-class-docstring

from typing import Any, Dict, Mapping, cast

from reporter.base import RestManager, RestObject

__all__ = [
    "Announcement",
    "AnnouncementManager",
]


class Announcement(RestObject):
    """Placeholder type for announcements.

    The announcements endpoint does not return a resource object; the manager's
    :meth:`AnnouncementManager.send` returns a plain dict instead.
    """


class AnnouncementManager(RestManager):
    _path = "announcements"
    _obj_cls = Announcement

    def send(self, attrs: Mapping[str, Any], **kwargs: Any) -> Dict[str, Any]:
        """Send an announcement.

        Args:
            attrs: Attributes for the announcement. Required fields: ``title``,
                ``body``, ``send_to``, ``user_activity``. Optional: ``channel``,
                ``clients``, ``active_since``, ``ttl``.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The raw response dict, e.g. ``{"success": True, "recipients": <int>}``.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        result = self.reporter.http_request(
            verb="post",
            path=self._path,
            post_data=attrs,
            **kwargs,
        )
        return cast(Dict[str, Any], result.json())
