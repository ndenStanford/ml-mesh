"""Prompt Exceptions."""

# Source
from src.exceptions import BasePromptException


class ModelNotFound(BasePromptException):
    """Prompt Not Found."""

    message_format = "Model '{model_name}' was not found in database."
