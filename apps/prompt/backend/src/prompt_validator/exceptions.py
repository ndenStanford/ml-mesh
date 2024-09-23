"""Exceptions."""

# Internal libraries
from onclusiveml.core.base.exception import OnclusiveException


class PromptInjectionException(OnclusiveException):
    """Prompt injection exception."""

    message_format = "Prompt injection detected: '{prompt}'"
