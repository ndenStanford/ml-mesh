"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class LanguageFilterException(OnclusiveException):
    """Language filter exception."""

    message_format = (
        "The language '{language_iso}' that was looked up from '{original_language}' or inferred "
        "from the content, is currently not supported. Supported languages are: "
        "{supported_language_isos}."
    )


class LanguageDetectionException(OnclusiveException):
    """Language detection exception."""

    message_format = (
        "The language reference '{original_language}' could not be mapped, or the language could "
        "not be inferred from the content. Supported references are: "
        "{supported_language_iso_values}. Supported languages are: {supported_language_isos}."
    )
