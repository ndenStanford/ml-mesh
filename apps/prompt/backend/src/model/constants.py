"""Constants."""

# Standard Library
from typing import List

# 3rd party libraries
from pydantic import Field

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel, OnclusiveEnum


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
    CLAUDE_3_5_SONNET = "anthropic.claude-3-5-sonnet-20240620-v1:0"
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


class BaseLLMParameters(OnclusiveBaseModel):
    """Base LLM parameters."""

    temperature: float = 0.7
    max_tokens: int = Field(3000, alias="maxTokens")


class TextGenerationConfig(BaseLLMParameters):
    """Text generation config for tital model parameters."""

    temperature: float = Field(0.7, alias="temperature")
    topP: float = Field(0.9, alias="topP")
    maxTokenCount: int = Field(512, alias="maxTokens")
    stopSequences: List[str] = Field([], alias="stopSequences")


class TitanParameters(OnclusiveBaseModel):
    """Tital model parameters."""

    textGenerationConfig: TextGenerationConfig = Field(
        ..., alias="textGenerationConfig"
    )


class Claude2Parameters(BaseLLMParameters):
    """Claude2 model parameters."""

    temperature: float = 0.5
    top_p: float = Field(1.0, alias="topP")
    top_k: int = Field(250, alias="topK")
    stop_sequences: List[str] = Field([], alias="stopSequences")


class Claude3Parameters(BaseLLMParameters):
    """Claude3 model parameters."""

    temperature: float = 1.0
    top_p: float = Field(0.999, alias="topP")
    top_k: float = Field(250, alias="topK")
    max_tokens: int = Field(50000, alias="maxTokens")
    stop_sequences: List[str] = Field([], alias="stopSequences")


class LlamaParameters(BaseLLMParameters):
    """Llama model parameters."""

    temperature: float = 0.5
    top_p: float = Field(0.9, alias="topP")
    max_gen_len: float = Field(512, alias="maxTokens")


class MistralInstructParameters(BaseLLMParameters):
    """Mistral instruct model parameters."""

    temperature: float = 0.5
    top_p: float = Field(0.9, alias="topP")
    top_k: float = Field(50, alias="topK")
    max_gen_len: float = Field(512, alias="maxTokens")
    stop: List[str] = Field([], alias="stopSequences")


class MistralLargeParameters(BaseLLMParameters):
    """Mistral Large model parameters."""

    temperature: float = 0.7
    top_p: float = Field(0.9, alias="topP")
    top_k: float = Field(50, alias="topK")
    max_gen_len: float = Field(512, alias="maxTokens")
    stop: List[str] = Field([], alias="stopSequences")


MODELS_TO_PARAMETERS = {
    ChatModel.GPT3_5: BaseLLMParameters,
    ChatModel.GPT4: BaseLLMParameters,
    ChatModel.GPT3_5_TURBO: BaseLLMParameters,
    ChatModel.GPT4_TURBO: BaseLLMParameters,
    ChatModel.GPT4_TURBO_PREVIEW: BaseLLMParameters,
    ChatModel.GPT4_O: BaseLLMParameters,
    ChatModel.GPT4_1106: BaseLLMParameters,
    ChatModel.TITAN: TitanParameters,
    ChatModel.TITAN_G1: TitanParameters,
    ChatModel.CLAUDE_2: Claude2Parameters,
    ChatModel.CLAUDE_2_1: Claude2Parameters,
    ChatModel.CLAUDE_3_5_SONNET: Claude3Parameters,
    ChatModel.CLAUDE_3_SONNET: Claude3Parameters,
    ChatModel.CLAUDE_3_HAIKU: Claude3Parameters,
    ChatModel.CLAUDE_3_INSTANT: Claude3Parameters,
    ChatModel.LLAMA_2_13B: LlamaParameters,
    ChatModel.LLAMA_2_70B: LlamaParameters,
    ChatModel.INSTRUCT_7B: MistralInstructParameters,
    ChatModel.INSTRUCT_8_7B: MistralInstructParameters,
    ChatModel.MISTRAL_LARGE: MistralLargeParameters,
}
# DEFAULT models
DEFAULT_MODELS = [
    {"alias": ChatModel.CLAUDE_2, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_2_1, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_3_SONNET, "provider": ChatModelProdiver.BEDROCK},
    {"alias": ChatModel.CLAUDE_3_5_SONNET, "provider": ChatModelProdiver.BEDROCK},
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
