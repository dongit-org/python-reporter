# pylint: disable = missing-module-docstring, missing-class-docstring
from reporter.base import RestManager
from reporter.mixins import CreateMixin
from reporter.objects.assessment_section_comment import AssessmentSectionComment

__all__ = [
    "AssessmentSectionEventReplyManager",
]


class AssessmentSectionEventReplyManager(RestManager, CreateMixin):
    _path = "assessment-section-events/{assessment_section_event_id}/assessment-section-comments"
    _parent_attrs = {"assessment_section_event_id": "id"}
    _obj_cls = AssessmentSectionComment
