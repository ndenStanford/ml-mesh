"""Generated Exceptions."""

# Source
from src.exceptions import BasePromptException


class GeneratedNotFound(BasePromptException):
    """Generated Not Found."""

    message_format = "Generated with id '{id}' was not found in database."


class GeneratedExisting(BasePromptException):
    """Generated already exists."""

    message_format = "Generated with id '{id}' already exists in database."


class GeneratedInvalidId(BasePromptException):
    """Generated Not Found."""

    message_format = "Generated id: '{id}' is invalid"


class GeneratedCreationImpossible(BasePromptException):
    """Generated not created (if generated_creation function did not return 200)."""

    message_format = "Generated with id '{id}' cannot be created at the moment."


class DeletionProtectedGenerated(BasePromptException):
    """Generated Deletion impossible (if generated_deletion function did not return 200)."""

    message_format = "Generated with id '{generated_id}' cannot be deleted."
