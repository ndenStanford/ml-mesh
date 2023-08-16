"""Prompt Exceptions."""

# Source
from src.exceptions import BasePromptException


class PromptNotFound(BasePromptException):
    """Prompt Not Found."""

    message_format = "Prompt '{alias}' was not found in database."


class PromptInvalidTemplate(BasePromptException):
    """Prompt Not Found."""

    message_format = "Prompt template: '{template}' is invalid"


class PromptVersionNotFound(BasePromptException):
    """Prompt Version Not Found."""

    message_format = (
        "Version '{version}' of prompt '{alias}' was not found in database."
    )


class DeletionProtectedPrompt(BasePromptException):
    """Attempt to delete deletion Protected Prompt"""

    message_format = "Prompt '{alias}' cannot be deleted."
