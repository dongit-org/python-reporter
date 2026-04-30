# pylint: disable = missing-module-docstring, missing-class-docstring
from typing import Any, Mapping

from reporter.base import RestManager, RestObject
from reporter.mixins import (
    CreateMixin,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
)
from .assessment_section_comment import AssessmentSectionAssessmentSectionCommentManager

__all__ = [
    "AssessmentSection",
    "AssessmentSectionManager",
    "AssessmentAssessmentSectionManager",
]


class AssessmentSection(RestObject):
    comments: AssessmentSectionAssessmentSectionCommentManager


class AssessmentSectionManager(
    RestManager,
    DeleteMixin,
    GetMixin,
    ListMixin,
    UpdateMixin,
):
    _path = "assessment-sections"
    _obj_cls = AssessmentSection


class AssessmentAssessmentSectionManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/assessment-sections"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = AssessmentSection

    def reorder(self, attrs: Mapping[str, Any], **kwargs: Any) -> None:
        """Reorder all assessment sections within the parent assessment.

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
