"""Language model dynamoDB tables."""

# Standard Library
from typing import Any, Dict, Optional

# 3rd party libraries
import boto3
from botocore.config import Config
from dyntastic import Dyntastic
from langchain_aws.chat_models import ChatBedrock
from langchain_openai.chat_models import ChatOpenAI
from pydantic import ValidationError

# Internal libraries
from onclusiveml.llms.mixins import LangchainConvertibleMixin
from onclusiveml.llms.typing import LangchainT

# Source
from src.model.constants import (
    MODELS_TO_PARAMETERS,
    BaseLLMParameters,
    ChatModel,
    ChatModelProdiver,
    TitanParameters,
)
from src.settings import get_settings


settings = get_settings()
config = Config(read_timeout=settings.BEDROCK_READ_TIMEOUT)


class LanguageModel(Dyntastic, LangchainConvertibleMixin):
    """Language model."""

    __table_name__ = "model"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    provider: str
    model_parameters: str = None

    def as_langchain(self, **kwargs: Dict[str, Any]) -> Optional[LangchainT]:
        """Return model as langchain chat model."""
        self.model_parameters = kwargs.get("model_parameters", None)
        model_parameters_class = MODELS_TO_PARAMETERS.get(
            self.alias, MODELS_TO_PARAMETERS[ChatModel.GPT4_O_MINI]
        )
        if self.provider == ChatModelProdiver.OPENAI:
            return self._handle_openai_provider(model_parameters_class)
        elif self.provider == ChatModelProdiver.BEDROCK:
            return self._handle_bedrock_provider(model_parameters_class)
        return None

    def _handle_openai_provider(
        self, model_parameters_class: BaseLLMParameters
    ) -> Optional[LangchainT]:
        """Handle the OpenAI provider specifics."""
        self._initialize_openai_model_parameters(model_parameters_class)
        return ChatOpenAI(
            model=self.alias,
            temperature=self.model_parameters.temperature,
            max_tokens=self.model_parameters.max_tokens,
        )

    def _handle_bedrock_provider(
        self, model_parameters_class: BaseLLMParameters
    ) -> Optional[LangchainT]:
        """Handle the Bedrock provider specifics."""
        self._initialize_bedrock_model_parameters(model_parameters_class)
        bedrock = self.bedrock_client
        return ChatBedrock(
            client=bedrock,
            model_id=self.alias,
            model_kwargs=self.model_parameters,
        )

    def _initialize_openai_model_parameters(
        self, model_parameters_class: BaseLLMParameters
    ):
        """Initialize the openai model parameters."""
        if self.model_parameters is None:
            self.model_parameters = model_parameters_class()
        else:
            try:
                self.model_parameters = model_parameters_class(**self.model_parameters)
            except ValidationError as e:
                raise ValueError(f"Invalid parameters: {e}")

    def _initialize_bedrock_model_parameters(
        self, model_parameters_class: BaseLLMParameters
    ):
        """Initialize the Bedrock model parameters."""
        if self.model_parameters is None:
            self.model_parameters = model_parameters_class().model_dump()
        else:
            try:
                if self.alias in [ChatModel.TITAN, ChatModel.TITAN_G1]:
                    self.model_parameters = TitanParameters(
                        **model_parameters_class(**self.model_parameters).model_dump()
                    ).model_dump()
                else:
                    self.model_parameters = model_parameters_class(
                        **self.model_parameters
                    ).model_dump()
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
            config=config,
        )
