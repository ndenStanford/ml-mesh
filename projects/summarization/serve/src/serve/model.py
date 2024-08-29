"""Prediction model."""

# Standard Library
import re
from typing import List, Optional, Type

# 3rd party libraries
import requests
from fastapi import HTTPException, status

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.core.logging import get_default_logger
from onclusiveml.core.system import SystemInfo
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.serving.client import OnclusiveApiClient
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.exceptions import (
    PromptBackendException,
    PromptNotFoundException,
    SummaryTypeNotSupportedException,
)
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

    @property
    def api_client(self) -> OnclusiveApiClient:
        """Translation service client."""
        return OnclusiveApiClient(
            host=settings.translation_api,
            api_key=settings.internal_ml_endpoint_api_key,
            secure=SystemInfo.in_kubernetes(),
        )

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": self.name, "model_card": {}},
        )

    def _identify_language(self, content: str) -> LanguageIso:
        """Detect input language.

        Args:
            content (str): input content
        """
        response = self.api_client.translation(
            content=content,
            source_language=None,
            target_language=None,
            translation=False,
        )

        return LanguageIso.from_language_iso(response.data.attributes.source_language)

    def _translate_sumary(
        self, content: str, input_language: LanguageIso, output_language: LanguageIso
    ) -> str:
        """Translate summary.

        Args:
            content (str): input content
            input_language (str): content language
            output_language (str): translation language
        """
        response = self.api_client.translation(
            content=content,
            source_language=input_language.value,
            target_language=output_language.value,
            translation=True,
        )
        return response.attributes.translated_text

    def _retrieve_prompt_alias(
        self, input_language: str, summary_type: str, multiple_article_summary: bool
    ) -> str:
        """Retrieves prompt alias.

        Args:
            input_language (str): input content language
            summary_type (str): summary type
            multiple_article_summary (bool): whether it is a multi-article summary
        """
        try:
            if not multiple_article_summary:
                alias = settings.summarization_prompts[input_language][summary_type]
            else:
                alias = settings.summarization_prompts[LanguageIso.EN][
                    settings.multi_article_summary
                ]
        except KeyError:
            raise PromptNotFoundException(
                language=input_language, summary_type=summary_type
            )
        return alias

    def _inference(
        self,
        content: str,
        prompt_alias: str,
        desired_length: int,
        keywords: List[str],
        title: bool,
        theme: Optional[str] = None,
    ) -> str:
        """Summarization prediction handler method.

        Args:
            content (str): Text to summarize
            prompt_alias (str): prompt template alias
            desired_length (int): desired length of the summary
            keywords (List[str]): relevant keywords/topics in the content for creating the summary
            title (bool): if title has to be returned
            theme (str): specific theme in the content for creating the summary
        """
        input_dict = {
            "input": {
                "desired_length": desired_length,
                "content": content,
                "keywords": ", ".join(keywords),
                "theme": theme,
            }
        }
        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}

        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.prompt_api, prompt_alias, settings.summarization_default_model
            ),
            headers=headers,
            json=input_dict,
        )

        if q.status_code == 200:
            return eval(q.content)["generated"]
        else:
            raise PromptBackendException(message=str(q.content))

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction.

        Args:
            payload (PredictRequestSchema): prediction request payload.
        """
        parameters = payload.parameters
        content = payload.attributes.content
        input_language = LanguageIso.from_language_iso(
            payload.parameters.input_language
        )
        output_language = LanguageIso.from_language_iso(
            payload.parameters.output_language
        )
        # identify language (needed to retrieve the appropriate prompt)
        multiple_article_summary = False
        try:
            content = eval(content)
        except Exception as e:
            logger.warn("Cannot eval content. Assuming it to be string type.", e)
        if type(content) == list:
            multiple_article_summary = True
            content = {
                f"Article {i}": f"```{article}```" for i, article in enumerate(content)
            }
        if input_language is None:
            input_language = self._identify_language(content)
            logger.debug(f"Detected content language: {input_language}")
        if output_language is None:
            output_language = input_language
        # retrieve prompt
        # depending on request parameters, we can determine what prompt to use.
        if parameters.summary_type not in ("bespoke", "section"):
            raise SummaryTypeNotSupportedException(summary_type=parameters.summary_type)

        try:
            prompt_alias = self._retrieve_prompt_alias(
                input_language=input_language,
                summary_type=parameters.summary_type,
                multiple_article_summary=multiple_article_summary,
            )
        except LanguageNotSupportedException as e:
            logger.error(f"Summarization language {input_language} not supported.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        logger.debug(f"Using the prompt {prompt_alias}")
        # content should no be empty.
        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no summary being returned"
            )

        content = re.sub("\n+", " ", str(content))

        summary = self._inference(
            content=content,
            desired_length=parameters.desired_length,
            keywords=parameters.keywords,
            title=parameters.title,
            theme=parameters.theme,
            prompt_alias=prompt_alias,
        )

        summary = re.sub("\n+", " ", summary)

        if not input_language == output_language:
            summary = self._translate_sumary(
                content=summary,
                input_language=input_language,
                output_language=output_language,
            )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"summary": summary},
        )
