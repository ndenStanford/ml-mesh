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
    """Attempt to delete deletion Protected Prompt."""

    message_format = "Prompt '{alias}' cannot be deleted."


class PromptInvalidParameters(BasePromptException):
    """Invalid Parameters."""

    message_format = "Parameter {param_name} = {param}, is invalid"


class PromptTokenExceedModel(BasePromptException):
    """Max token limit exceeded for model."""

    message_format = "Parameter max_tokens must be between 1 and {max_token_length} for model {model}"  # noqa: E501


class PromptOutsideTempLimit(BasePromptException):
    """Temperature is beyond limit."""

    message_format = "Temperature must be between 0.0 and 1.0"


class PromptModelUnsupported(BasePromptException):
    """Model is not supported."""

    message_format = "{model} is not supported"


class StrOutputParserTypeError(BasePromptException):
    """str_output_parser is not a boolean."""

    message_format = "str_output_parser must be a boolean value"


class PromptFieldsMissing(BasePromptException):
    """Prompt fields missing."""

    message_format = "Prompt fields must exist if str_output_parser is True."
