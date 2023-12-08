"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class LanguageFilterException(OnclusiveException):
    """Language filter exception."""

    message_format = (
        "The language '{language_iso}', is currently not supported. Supported languages are: "
        "{supported_language_isos}."
    )


class LanguageDetectionException(OnclusiveException):
    """Language detection exception."""

    message_format = (
        "The language reference '{language_iso_value}' could not be mapped. Supported references "
        "are {supported_language_iso_values}. Supported languages are {supported_language_isos}."
    )
