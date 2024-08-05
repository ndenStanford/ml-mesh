"""Exceptions."""

# Internal libraries
from onclusiveml.core.base import OnclusiveException


class FileIOException(OnclusiveException):
    """Unknown I/O error."""

    message_format = "File I/O exception: {message}"


class UnknownFileSystemException(FileIOException):
    """Unknown filesystem error."""

    message_format = "The filesystem {fs} is not supported."


class UncompatiblePathException(OnclusiveException):
    """Incompatible Path."""

    message_format = "Path {path} is not compatible with filesystem {fs}."
