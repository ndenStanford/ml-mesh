"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class LanguageNotSupportedException(OnclusiveException):
    """Language not supported exception."""

    message_format = (
        "Summary language '{language}' and or '{summary_type}' not supported."
    )


class PromptBackendException(OnclusiveException):
    """Language not supported exception."""

    message_format = "Prompt backend error: {message}."


class SummaryTypeNotSupportedException(OnclusiveException):
    """Summary type not supported exception."""

    message_format = "Summary type: {summary_type} not supported."
