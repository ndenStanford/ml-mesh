"""Prompt Exceptions."""

# Source
from src.exceptions import BasePromptException


class PromptException(BasePromptException):
    """Generic prompt exception."""

    message_format = "Prompt exception."
