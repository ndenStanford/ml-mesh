"""Constants."""

# Internal libraries
from onclusiveml.core.base.utils import OnclusiveEnum


class ChatModel(str, OnclusiveEnum):
    """Chat models."""

    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT3_5_TURBO = "gpt-3.5-turbo-1106"
    GPT4_TURBO = "gpt-4-1106-preview"


class ChatModelProdiver(str, OnclusiveEnum):
    """Enum values for chat model providers."""

    OPENAI: str = "openai"
    BEDROCK: str = "bedrock"


DEFAULT_MODELS = [
    {"alias": ChatModel.GPT3_5, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT3_5_TURBO, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4_TURBO, "provider": ChatModelProdiver.OPENAI},
]
