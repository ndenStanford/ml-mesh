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

    def identify_language(text):
        """Detect input language."""
        payload = {
            "data": {
                "identifier": "None",
                "namespace": "translation",
                "attributes": {"content": text},
                "parameters": {},
            }
        }
        headers = {
            "content-type": "application/json",
            "x-api-key": settings.internal_ml_endpoint_api_key,
        }

        response = requests.post(
            f"{settings.translation_api}/translation/v1/predict",
            json=payload,
            headers=headers,
        )

        return response["data"]["attributes"]["source_language"]

    def inference(
        self,
        text,
        desired_length,
        input_language,
        output_language,
        type,
        keywords,
        title,
        theme,
    ) -> str:
        """Summarization prediction handler method.

        Args:
            text (str): Text to summarize
            desired_length (int): desired length of the summary
            input_language (str): input language of the summary
            output_language (str): target language
            type (str): summary type between bespoke-summary and section-summary
            keywords (List(str)): relevant keywords/topics in the content for creating the summary
            title (bool): if title has to be returned
            theme (str): specific theme in the content for creating the summary
        """
        try:
            if input_language is None:
                input_language = self.identify_language(text)
            if output_language is None:
                output_language = input_language

            if type == "bespoke-summary":
                alias = settings.summarization_prompts[input_language][output_language][
                    "bespoke-summary"
                ]["alias"]
            else:
                alias = settings.summarization_prompts[input_language][output_language][
                    "alias"
                ]

        except KeyError:
            logger.error("Summarization language not supported.")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Unsupported language",
            )

        input_dict = {
            "input": {
                "desired_length": desired_length,
                "content": text,
                "keywords": keywords,
                "theme": theme,
            }
        }
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
        input_language = parameters.input_language
        desired_length = parameters.desired_length
        output_language = parameters.output_language
        type = parameters.type
        keywords = parameters.keywords
        title = parameters.title
        theme = parameters.theme

        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no summary being returned"
            )

        text = re.sub("\n+", " ", content)
        summary = self.inference(
            text,
            desired_length,
            input_language,
            output_language,
            type,
            keywords,
            title,
            theme,
        )
        summary = re.sub("\n+", " ", summary)

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"summary": summary},
        )
