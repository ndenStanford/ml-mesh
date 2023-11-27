"""Constants."""

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


class ModelEnum_chat(OnclusiveEnum):
    """Enum values for chat models."""

    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT3_5_turbo = "gpt-3.5-turbo-1106"
    GPT4_turbo = "gpt-4-1106-preview"


class ModelEnum_completions(OnclusiveEnum):
    """Enum values for completions models."""

    GPT3_5_instruct = "gpt-3.5-turbo-instruct"
