"""Prompt Exceptions."""

# Source
from src.exceptions import BasePromptException


class ProjectNotFound(BasePromptException):
    """Project Not Found."""

    message_format = "Project '{alias}' was not found in database."


class ProjectsNotFound(BasePromptException):
    """Projects Not Found."""

    message_format = "Projects not found in database."


class ProjectsExisting(BasePromptException):
    """Projects Not Found."""

    message_format = "Project '{alias}' already exists in database."


class ProjectInvalidAlias(BasePromptException):
    """Project Not Found."""

    message_format = "Project template: '{alias}' is invalid"


class CreationProjectImpossible(BasePromptException):
    """Project not created (if project_creation function did not return 200)."""

    message_format = "Project '{alias}' cannot be created at the moment."


class DeletionProtectedProject(BasePromptException):
    """Delete impossible (if project_deletion function did not return 200)."""

    message_format = "Project '{alias}' cannot be deleted."


class ProjectTokenExceedAlias(BasePromptException):
    """Max token limit exceeded for model."""

    message_format = "Project alias too long"
