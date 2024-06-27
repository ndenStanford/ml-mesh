"""Constants."""

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.utils import OnclusiveEnum


class ChatModel(str, OnclusiveEnum):
    """Chat models.

    References:
        Bedrock: https://docs.aws.amazon.com/bedrock/latest/userguide/model-ids.html
    """

    GPT3_5 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    GPT3_5_TURBO = "gpt-3.5-turbo-1106"
    GPT4_TURBO = "gpt-4-turbo-2024-04-09"
    GPT4_TURBO_PREVIEW = "gpt-4-0125-preview"
    GPT4_O = "gpt-4o"
    GPT4_1106 = "gpt-4-1106-preview"
    TITAN = "amazon.titan-text-express-v1"
    TITAN_G1 = "amazon.titan-text-lite-v1"
    CLAUDE_2 = "anthropic.claude-v2"
    CLAUDE_2_1 = "anthropic.claude-v2:1"
    CLAUDE_3_SONNET = "anthropic.claude-3-sonnet-20240229-v1:0"
    CLAUDE_3_HAIKU = "anthropic.claude-3-haiku-20240307-v1:0"
    CLAUDE_3_INSTANT = "anthropic.claude-instant-v1"
    LLAMA_2_13B = "meta.llama2-13b-chat-v1"
    LLAMA_2_70B = "meta.llama2-70b-chat-v1"
    INSTRUCT_7B = "mistral.mistral-7b-instruct-v0:2"
    INSTRUCT_8_7B = "mistral.mixtral-8x7b-instruct-v0:1"
    MISTRAL_LARGE = "mistral.mistral-large-2402-v1:0"


class ChatModelProdiver(str, OnclusiveEnum):
    """Enum values for chat model providers."""

    OPENAI: str = "openai"
    BEDROCK: str = "bedrock"


class ModelParameters(OnclusiveBaseSettings):
    """Default model parameters."""

    max_tokens: int = 50000
    temperature: float = 0.7


# DEFAULT models
DEFAULT_MODELS = [
    {"alias": ChatModel.CLAUDE_2, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_2_1, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_3_SONNET, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_3_HAIKU, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_3_INSTANT, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.GPT3_5, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT3_5_TURBO, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4_TURBO_PREVIEW, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4_TURBO, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4_1106, "provider": ChatModelProdiver.OPENAI},
    {"alias": ChatModel.GPT4_O, "provider": ChatModelProdiver.OPENAI},
]
