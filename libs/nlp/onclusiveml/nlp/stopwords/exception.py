"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class StopwordsFileException(OnclusiveException):
    """Stop words file exception."""

    message_format = "No stopword file found for {language}"
