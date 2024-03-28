"""Language model dynamoDB tables."""

# Standard Library
from typing import Optional, Type

# 3rd party libraries
from dyntastic import Dyntastic
from langchain.chat_models import ChatOpenAI
from langchain.chat_models.base import BaseChatModel

# Source
from src.model.constants import ChatModelProdiver
from src.settings import get_settings


settings = get_settings()


class LanguageModel(Dyntastic):
    __table_name__ = "model"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    provider: str
    parameters: dict = {}

    def as_langchain(self) -> Optional[BaseChatModel]:
        """Return model as langchain chat model."""
        if self.provider == ChatModelProdiver.OPENAI:
            return ChatOpenAI(model=self.alias, **self.parameters)
        return None
