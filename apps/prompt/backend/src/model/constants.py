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


class OpenaiModelParameters(OnclusiveBaseSettings):
    """OPENAI model parameters."""

    temperature: float = 0.7
    max_tokens: int = 50000


class BedrockModelParameters(OnclusiveBaseSettings):
    """Bedrock model parameters."""

    titan: dict = {
        "textGenerationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxTokenCount": 512,
            "stopSequences": [],
        }
    }
    titan_g1: dict = {
        "textGenerationConfig": {
            "temperature": 0.7,
            "topP": 0.9,
            "maxTokenCount": 512,
            "stopSequences": [],
        }
    }
    cluade_2: dict = {
        "temperature": 0.5,
        "top_p": 1.0,
        "top_k": 250,
        "max_tokens_to_sample": 200,
        "stop_sequences": [],
    }
    cluade_2_1: dict = {
        "temperature": 0.5,
        "top_p": 1.0,
        "top_k": 250,
        "max_tokens_to_sample": 200,
        "stop_sequences": [],
    }
    claude_3_sonnet: dict = {
        "temperature": 1.0,
        "top_p": 0.999,
        "top_k": 250,
        "max_tokens": 50000,
        "stop_sequences": [],
    }
    claude_3_haiku: dict = {
        "temperature": 1.0,
        "top_p": 0.999,
        "top_k": 250,
        "max_tokens": 50000,
        "stop_sequences": [],
    }
    claude_3_instant: dict = {
        "temperature": 1.0,
        "top_p": 0.999,
        "top_k": 250,
        "max_tokens": 50000,
        "stop_sequences": [],
    }
    llama_2_13b: dict = {"temperature": 0.5, "top_p": 0.9, "max_gen_len": 512}
    llama_2_70b: dict = {"temperature": 0.5, "top_p": 0.9, "max_gen_len": 512}
    instruct_7B: dict = {
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50,
        "stop": [],
    }
    instruct_8_7B: dict = {
        "max_tokens": 512,
        "temperature": 0.5,
        "top_p": 0.9,
        "top_k": 50,
        "stop": [],
    }
    mistral_large: dict = {
        "max_tokens": 8192,
        "temperature": 0.7,
        "top_p": 1.0,
        "stop": [],
    }

    class Config:
        env_prefix = "params_"


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
