# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RestManager, RestObject
from reporter.mixins import CreateMixin, DeleteMixin


__all__ = [
    "OutputFile",
    "OutputFileManager",
    "AssessmentOutputFileManager",
]


class OutputFile(RestObject):
    pass


class OutputFileManager(RestManager, DeleteMixin):
    _path = "output-files"
    _obj_cls = OutputFile


class AssessmentOutputFileManager(RestManager, CreateMixin):
    _path = "assessments/{assessment_id}/output-files"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = OutputFile
