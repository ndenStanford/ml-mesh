"""Language model dynamoDB tables."""

# Standard Library
from typing import Any, Optional

# 3rd party libraries
import boto3
from dyntastic import Dyntastic
from langchain_community.chat_models import BedrockChat, ChatOpenAI
from pydantic import ValidationError

# Internal libraries
from onclusiveml.llms.mixins import LangchainConvertibleMixin
from onclusiveml.llms.typing import LangchainT

# Source
from src.model.constants import (
    MODELS_TO_PARAMETERS,
    ChatModel,
    ChatModelProdiver,
    TitanParameters,
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
    model_parameters: str = None

    def as_langchain(self, **kwargs) -> Optional[LangchainT]:
        """Return model as langchain chat model."""
        self.model_parameters = kwargs.get("model_parameters", None)
        model_params_class = MODELS_TO_PARAMETERS.get(
            self.alias, MODELS_TO_PARAMETERS[ChatModel.CLAUDE_3_HAIKU]
        )
        if self.provider == ChatModelProdiver.OPENAI:
            return self._handle_openai_provider(model_params_class)
        elif self.provider == ChatModelProdiver.BEDROCK:
            return self._handle_bedrock_provider(model_params_class)
        return None

    def _handle_openai_provider(self, model_params_class) -> Optional[LangchainT]:
        """Handle the OpenAI provider specifics."""
        self._initialize_openai_parameters(model_params_class)
        return ChatOpenAI(
            model=self.alias,
            temperature=self.model_parameters.temperature,
            max_tokens=self.model_parameters.max_tokens,
        )

    def _handle_bedrock_provider(self, model_params_class) -> Optional[LangchainT]:
        """Handle the Bedrock provider specifics."""
        self._initialize_bedrock_model_params(model_params_class)
        bedrock = self.bedrock_client
        return BedrockChat(
            client=bedrock,
            model_id=self.alias,
            model_kwargs=self.model_parameters,
        )

    def _initialize_openai_parameters(self, model_params_class):
        """Initialize the openai model parameters."""
        if self.model_parameters is None:
            self.model_parameters = model_params_class()
        else:
            try:
                self.model_parameters = model_params_class(**self.model_parameters)
            except ValidationError as e:
                raise ValueError(f"Invalid parameters: {e}")

    def _initialize_bedrock_model_params(self, model_params_class):
        """Initialize the Bedrock model parameters."""
        if self.model_parameters is None:
            self.model_parameters = model_params_class().dict()
        else:
            try:
                if self.alias in [ChatModel.TITAN, ChatModel.TITAN_G1]:
                    self.model_parameters = TitanParameters(
                        **model_params_class(**self.model_parameters).dict()
                    ).dict()
                else:
                    self.model_parameters = model_params_class(
                        **self.model_parameters
                    ).dict()
            except ValidationError as e:
                raise ValueError(f"Invalid parameters: {e}")

    @property
    def boto3_session(self) -> Any:
        """Setup boto3 session."""
        boto3.setup_default_session(
            profile_name=settings.AWS_PROFILE,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )
        return boto3.Session()

    @property
    def bedrock_client(self) -> Any:
        """Create a Bedrock client."""
        return self.boto3_session.client(
            service_name="bedrock-runtime",
            region_name=settings.AWS_DEFAULT_REGION,
            endpoint_url="https://bedrock-runtime.us-east-1.amazonaws.com",
        )
