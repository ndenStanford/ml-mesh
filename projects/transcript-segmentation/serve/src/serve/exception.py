"""Base Exception."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class PromptBackendUpstreamError(OnclusiveException):
    """Prompt backend upstream error."""

    message_format = "Error occured in prompt backend service"
