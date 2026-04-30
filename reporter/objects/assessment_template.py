# pylint: disable = missing-module-docstring, missing-class-docstring
from __future__ import annotations
from typing import Any, Mapping

from reporter.base import RestManager, RestObject
from reporter.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
)
from .assessment_section_template import (
    AssessmentTemplateAssessmentSectionTemplateManager,
)

__all__ = [
    "AssessmentTemplate",
    "AssessmentTemplateManager",
]


class AssessmentTemplate(RestObject):
    sections: AssessmentTemplateAssessmentSectionTemplateManager


class AssessmentTemplateManager(
    RestManager,
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "assessment-templates"
    _obj_cls = AssessmentTemplate

    def add_translation(
        self,
        id: str,  # pylint: disable = redefined-builtin
        attrs: Mapping[str, Any],
        **kwargs: Any,
    ) -> AssessmentTemplate:
        """Add a new language translation to an assessment template.

        Args:
            id: The ID of the assessment template.
            attrs: Attributes for the request. Must contain ``language_id``;
                may contain ``source_language_id``.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The updated assessment template.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        result = self.reporter.http_request(
            verb="post",
            path=f"{self._path}/{id}/add-translation",
            post_data=attrs,
            **kwargs,
        )
        return self._obj_cls(self.reporter, result.json())

    def destroy_translation(
        self,
        id: str,  # pylint: disable = redefined-builtin
        language_id: str,
        **kwargs: Any,
    ) -> AssessmentTemplate:
        """Remove a language translation from an assessment template.

        Args:
            id: The ID of the assessment template.
            language_id: The ID of the language whose translation to remove.
            kwargs: Extra options to pass to the underlying
                :func:`reporter.Reporter.http_request` call.

        Returns:
            The updated assessment template.

        Raises:
            ReporterHttpError: If raised by the underlying call to
                :func:`reporter.Reporter.http_request`.
        """
        result = self.reporter.http_request(
            verb="delete",
            path=f"{self._path}/{id}/languages/{language_id}",
            **kwargs,
        )
        return self._obj_cls(self.reporter, result.json())
