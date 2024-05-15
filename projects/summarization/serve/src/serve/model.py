"""Prediction model."""

# Standard Library
import re
from typing import Dict, Type

# 3rd party libraries
import requests
from pydantic import BaseModel

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()
logger = get_default_logger(__name__)


class SummarizationServedModel(ServedModel):
    """Summarization model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": self.name, "model_card": {}},
        )

    @property
    def headers(self) -> Dict[str, str]:
        """Request headers."""
        return {settings.api_key_name: settings.internal_ml_api_key.get_secret_value()}

    def inference(
        self,
        text: str,
        desired_length: int,
        lang: str,
        target_lang: str,
    ) -> str:
        """Summarization prediction handler method.

        Args:
            text (str): Text to summarize
            desired_length (int): desired length of the summary
            lang (str): input language of the summary
            target_lang (str): target language
        """
        try:
            alias = settings.PROMPT_DICT[lang][target_lang]["alias"]
        except KeyError:
            logger.errror("Summarization language not supported.")

        input_dict = {"input": {"desired_length": desired_length, "content": text}}
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )
        return eval(q.content)["generated"]

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        lang = parameters.language
        desired_length = parameters.desired_length
        target_lang = parameters.target_language

        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no summary being returned"
            )

        text = re.sub("\n+", " ", content)
        summary = self.inference(text, desired_length, lang, target_lang)
        summary = re.sub("\n+", " ", summary)

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"summary": summary},
        )
