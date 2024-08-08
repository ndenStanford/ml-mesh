"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class PromptNotFoundException(OnclusiveException):
    """Prompt not found exception."""

    message_format = "Prompt not found. Summary language '{language}' and or '{summary_type}' not supported."  # noqa: E501


class PromptBackendException(OnclusiveException):
    """Language not supported exception."""

    message_format = "Prompt backend error: {message}."


class SummaryTypeNotSupportedException(OnclusiveException):
    """Summary type not supported exception."""

    message_format = "Summary type: {summary_type} not supported."
