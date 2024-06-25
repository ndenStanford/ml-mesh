"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class PromptBackendError(OnclusiveException):
    """Prompt backend error exception."""

    message_format = "Error occured in prompt backend service '{error}"
