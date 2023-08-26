"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class LanguageFilterException(OnclusiveException):
    message_format = "The language, '{language}', is currently not supported."


class LanguageDetectionException(OnclusiveException):
    message_format = "The language, '{language}', cannot be found"
