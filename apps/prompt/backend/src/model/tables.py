"""Language model dynamoDB tables."""

# Standard Library
from typing import Any, Dict, Optional

# 3rd party libraries
import boto3
from dyntastic import Dyntastic
from fastapi import Header
from langchain_community.chat_models import BedrockChat, ChatOpenAI

# Internal libraries
from onclusiveml.llms.mixins import LangchainConvertibleMixin
from onclusiveml.llms.typing import LangchainT

# Source
from src.model.constants import (
    BedrockModelParameters,
    ChatModel,
    ChatModelProdiver,
    OpenaiModelParameters,
)
from src.settings import get_settings


settings = get_settings()


class LanguageModel(Dyntastic, LangchainConvertibleMixin):
    """Language model."""

    __table_name__ = "model"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    provider: str
    model_params: Dict[str, Any] = Header(None)

    def as_langchain(self) -> Optional[LangchainT]:
        """Return model as langchain chat model."""
        if self.provider == ChatModelProdiver.OPENAI:
            if self.model_params is None:
                self.model_params = OpenaiModelParameters()
            return ChatOpenAI(
                model=self.alias,
                temperature=model_params.temperature,
                max_tokens=model_params.max_tokens,
            )
        if self.provider == ChatModelProdiver.BEDROCK:
            print(self.model_params)
            if self.model_params is None:
                self.model_params = BedrockModelParameters().dict()
                print(self.model_params)
            boto3.setup_default_session(
                profile_name=settings.AWS_PROFILE,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            bedrock = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.AWS_DEFAULT_REGION,
                endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com",
            )
            chat_models = dict(map(lambda item: (item.value, item.name), ChatModel))
            return BedrockChat(
                client=bedrock,
                model_id=self.alias,
                model_kwargs=self.model_params[f"{chat_models[self.alias]}".lower()],
            )
        return None
