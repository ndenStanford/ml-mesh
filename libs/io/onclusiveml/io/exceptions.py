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


class IncompatibleSchemesException(OnclusiveException):
    """Incompatible schemss."""

    message_format = "Got schemes {scheme_source} and {scheme_destination} but expected {scheme_source_expected} and {scheme_destination_expected}."  # noqa: E501
