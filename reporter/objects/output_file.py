# pylint: disable = missing-module-docstring, missing-class-docstring

from reporter.base import RESTManager, RESTObject
from reporter.mixins import CreateMixin, DeleteMixin


__all__ = [
    "OutputFile",
    "OutputFileManager",
    "AssessmentOutputFileManager",
]


class OutputFile(RESTObject):
    pass


class OutputFileManager(RESTManager, DeleteMixin):
    _path = "output-files"
    _obj_cls = OutputFile


class AssessmentOutputFileManager(RESTManager, CreateMixin):
    _path = "assessments/{assessment_id}/output-files"
    _parent_attrs = {"assessment_id": "id"}
    _obj_cls = OutputFile
