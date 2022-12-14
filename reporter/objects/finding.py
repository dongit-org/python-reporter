# pylint: disable = missing-module-docstring, missing-class-docstring

from typing import Any, Dict, TYPE_CHECKING
from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin, GetMixin, ListMixin, UpdateMixin

__all__ = [
    "Finding",
    "FindingManager",
    "AssessmentFindingManager",
]


class Finding(RestObject):
    pass


class FindingManager(RestManager, DeleteMixin, GetMixin, ListMixin, UpdateMixin):
    _path = "findings"
    _obj_cls = Finding


class AssessmentFindingManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/findings"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = Finding

    def create_from_template(
        self, template_id: str, attrs: Dict[str, Any], **kwargs: Any
    ) -> Finding:
        """Create a new finding from a finding template

        Args:
            template_id: The ID of the finding template.
            attrs: Attributes for the created finding.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The response from the server, serialized into the `Finding` type.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.

        """
        if TYPE_CHECKING:
            assert isinstance(self._parent, RestObject)
        path = f"assessments/{self._parent.id}/finding-templates/{template_id}/findings"
        result = self.reporter.http_request(
            verb="post",
            path=path,
            post_data=attrs,
            files=None,
            **kwargs,
        )
        if TYPE_CHECKING:
            assert isinstance(result, dict)
        return Finding(self.reporter, result.json())
