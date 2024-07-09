"""Prediction model."""

# Standard Library
import re
from typing import Type

# 3rd party libraries
import requests
from fastapi import HTTPException, status

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
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

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": self.name, "model_card": {}},
        )

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
            alias = settings.summarization_prompts[lang][target_lang]["alias"]
        except KeyError:
            logger.error("Summarization language not supported.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unsupported language",
            )

        input_dict = {"input": {"desired_length": desired_length, "content": text}}
        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}

        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.prompt_api, alias, settings.summarization_default_model
            ),
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
