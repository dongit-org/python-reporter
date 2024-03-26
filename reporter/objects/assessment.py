# pylint: disable = missing-module-docstring, missing-class-docstring, redefined-builtin
from typing import Any

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, GetMixin, ListMixin, UpdateMixin, DeleteMixin


__all__ = [
    "Assessment",
    "AssessmentManager",
    "ClientAssessmentManager",
]


class Assessment(RestObject):
    pass


class AssessmentManager(RestManager, GetMixin, ListMixin, UpdateMixin, DeleteMixin):
    _path = "assessments"
    _obj_cls = Assessment

    def get_full_report(self, id, **kwargs: Any) -> bytes:
        """Get the full PDF report of an assessment.

        Args:
            id: The ID of the assessment
            **kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The full report as a bytestring.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = f"{self._path}/{id}/pdf-reports/full"

        result = self.reporter.http_request(
            verb="get",
            path=path,
            headers={"Accept": "*/*"},
            **kwargs,
        )

        return result.content

    def get_management_report(self, id, **kwargs: Any) -> bytes:
        """Get the management PDF report of an assessment.

        Args:
            id: The ID of the assessment
            **kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The management report as a bytestring.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        path = f"{self._path}/{id}/pdf-reports/management"

        return self.reporter.get_raw_file(path, **kwargs)


class ClientAssessmentManager(RestManager, CreateMixin):
    _path = "clients/{client_id}/assessments"
    _parent_attrs = {"client_id": "id"}
    _obj_cls = Assessment
