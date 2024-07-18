"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class PromptBackendException(OnclusiveException):
    """Prompt backend error exception."""

    message_format = "Error occured in prompt backend service: '{error}"


class StructuredOutputException(OnclusiveException):
    """JSON or structuredOutput error exception."""

    message_format = "JSON or StructuredOutput Error: '{error}"
