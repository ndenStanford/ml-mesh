"""Language model dynamoDB tables."""

# Standard Library
from typing import Optional, Type

# 3rd party libraries
import boto3
from dyntastic import Dyntastic
from langchain_community.chat_models import BedrockChat, ChatOpenAI

# Internal libraries
from onclusiveml.llm.mixins import LangchainConvertibleMixin
from onclusiveml.llm.typing import LangchainT

# Source
from src.model.constants import ChatModelProdiver
from src.settings import get_settings


settings = get_settings()


class LanguageModel(Dyntastic, LangchainConvertibleMixin):
    __table_name__ = "model"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    provider: str

    def as_langchain(self) -> Optional[LangchainT]:
        """Return model as langchain chat model."""
        if self.provider == ChatModelProdiver.OPENAI:
            return ChatOpenAI(model=self.alias)
        if self.provider == ChatModelProdiver.BEDROCK:
            session = boto3.setup_default_session(profile_name=settings.AWS_PROFILE)
            bedrock = boto3.client(
                service_name="bedrock-runtime",
                region_name=settings.AWS_DEFAULT_REGION,
                endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com",
            )
            return BedrockChat(client=bedrock, model_id=self.alias)
        return None
