"""Additional types used by this library."""
from __future__ import annotations
from typing import Protocol, TypeVar, TypeAlias, Optional, Union, Mapping

__all__ = [
    "FileContent",
    "FileSpec",
]

T_co = TypeVar("T_co", covariant=True)

class SupportsRead(Protocol[T_co]):
    """Protocol for objects that support read()."""
    def read(self, n: int = ...) -> T_co:
        """Read n bytes from the object."""

# File content can be a string, bytes, or file-like object
FileContent: TypeAlias = SupportsRead[str | bytes] | str | bytes
"""
Represents the content of a file, can be bytes, str, or a file-like object that supports read().
"""
FileName: TypeAlias = Optional[str]
FileContentType: TypeAlias = str
FileHeaders: TypeAlias = Mapping[str, str]
FileSpec: TypeAlias = Union[
    FileContent,
    tuple[FileName, FileContent],
    tuple[FileName, FileContent, FileContentType],
    tuple[FileName, FileContent, FileContentType, FileHeaders],
]
"""
Specification for a file, with optional name, type, and headers.

Can be one of the following:

- :class:`FileContent`: Raw file content (filename will be "file")
- tuple: ``(filename, file_content)`` or ``(filename, file_content, content_type)`` or
  ``(filename, file_content, content_type, headers)``
"""
