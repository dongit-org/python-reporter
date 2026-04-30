# pylint: disable = missing-module-docstring, missing-class-docstring, duplicate-code
from typing import Any, Mapping

from reporter.base import RestManager, RestObject
from reporter.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
)

__all__ = [
    "AssessmentSectionTemplate",
    "AssessmentSectionTemplateManager",
    "AssessmentTemplateAssessmentSectionTemplateManager",
]


class AssessmentSectionTemplate(RestObject):
    pass


class AssessmentSectionTemplateManager(
    RestManager,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "assessment-section-templates"
    _obj_cls = AssessmentSectionTemplate


class AssessmentTemplateAssessmentSectionTemplateManager(RestManager, CreateMixin):
    _path = "assessment-templates/{assessment_template_id}/assessment-section-templates"
    _parent_attrs = {"assessment_template_id": "id"}
    _obj_cls = AssessmentSectionTemplate

    def reorder(self, attrs: Mapping[str, Any], **kwargs: Any) -> None:
        """Reorder all section templates within the parent assessment template.

        Args:
            attrs: A mapping with a ``sections`` key containing a nested tree of
                sections by id (each entry may have a ``children`` list).
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        self.reporter.http_request(
            verb="post",
            path=f"{self._path}/reorder",
            post_data=attrs,
            **kwargs,
        )
