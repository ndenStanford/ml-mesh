"""Prediction model."""

# Standard Library
import re
from typing import List, Optional, Type, Union

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
    PromptInjectionException,
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

    def _translate(
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
            # Check if the input language exists in the summarization_prompts dictionary
            if input_language in LanguageIso and (
                input_language not in settings.summarization_prompts
                or summary_type not in settings.summarization_prompts[input_language]
            ):
                logger.warning(
                    f"Language {input_language} and summary_type {summary_type} currently not supported. Using English as default."
                )
                input_language = LanguageIso.EN

            if not multiple_article_summary:
                alias = settings.summarization_prompts[input_language][summary_type]
            else:
                alias = settings.summarization_prompts[LanguageIso.EN][
                    settings.multi_article_summary
                ][summary_type]
        except KeyError:
            raise PromptNotFoundException(
                language=input_language, summary_type=summary_type
            )
        return alias

    def _inference(
        self,
        content: Union[str, dict],
        prompt_alias: str,
        desired_length: int,
        keywords: List[str],
        title: bool,
        custom_instructions: Optional[List],
        theme: Optional[str] = None,
    ) -> str:
        """Summarization prediction handler method.

        Args:
            content (str or dict): Text to summarize
            prompt_alias (str): prompt template alias
            desired_length (int): desired length of the summary
            keywords (List[str]): relevant keywords/topics in the content for creating the summary
            title (bool): if title has to be returned
            theme (str): specific theme in the content for creating the summary
            custom_instructions (List): user instructions that define the requirements for the summary
        """
        input_dict = {
            "input": {
                "desired_length": desired_length,
                "content": content,
                "keywords": ", ".join(keywords),
                "theme": theme,
                "custom_instructions": custom_instructions,
            }
        }

        if title:
            input_dict["output"] = settings.output_schema_with_title

        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}

        q = requests.post(
            "{}/api/v3/prompts/{}/generate/model/{}".format(
                settings.prompt_api, prompt_alias, settings.summarization_default_model
            ),
            headers=headers,
            json=input_dict,
        )

        if q.status_code == 200:
            if title:
                return eval(q.content)
            else:
                return {"summary": eval(q.content)["generated"]}
        elif q.status_code == 400:
            raise PromptInjectionException(content=content)
        else:
            raise PromptBackendException(message=str(q.content))

    @staticmethod
    def _find_snippets(
        text: str, keywords: List[str], snippet_length: int
    ) -> List[str]:
        """Generates snippets of 150 characters around each occurrence of any keyword in the text."""
        snippets = []
        text_len = len(text)

        # Track if keywords exist in text
        keyword_found = False

        for keyword in keywords:
            keyword_pos = text.lower().find(keyword.lower())
            if keyword_pos != -1:
                keyword_found = True
                start = max(keyword_pos - int(snippet_length / 2), 0)
                end = min(keyword_pos + int(snippet_length / 2), text_len)
                snippet = text[start:end].strip()
                snippets.append(snippet)

        # If no keyword was found, add the first 150 characters once
        if not keyword_found and text_len > 0:
            snippets.append(text[:snippet_length].strip())

        return snippets

    def find_snippets(
        self,
        content: Union[List, str],
        keywords: List[str],
        multiple_article_summary: bool,
        snippet_length: int,
    ):
        """Extract snippets based on keywords."""
        if multiple_article_summary:
            all_snippets = []
            for text in content:
                all_snippets.extend(self._find_snippets(text, keywords, snippet_length))
            return all_snippets
        else:
            return self._find_snippets(content, keywords, snippet_length)

    def _prepare_content(self, content: Union[List, str], parameters: dict):
        """Prepare and validate content, handling multiple article cases."""
        if isinstance(content, list):
            multiple_article_summary = True
        elif isinstance(content, str):
            multiple_article_summary = False
        else:
            raise ValueError("Content must be a string or a list of strings.")

        if parameters.summary_type == settings.snippet_summary_type:
            content = self.find_snippets(
                content,
                parameters.keywords,
                multiple_article_summary,
                settings.snippet_length,
            )

        if multiple_article_summary:
            content = {
                f"Article {i}": f"```{article}```" for i, article in enumerate(content)
            }

        return content, multiple_article_summary

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction.

        Args:
            payload (PredictRequestSchema): prediction request payload.
        """
        parameters = payload.parameters
        content, multiple_article_summary = self._prepare_content(
            payload.attributes.content, parameters
        )

        if len(content) == 0:
            return PredictResponseSchema.from_data(
                version=int(settings.api_version[1:]),
                namespace=settings.model_name,
                attributes={"summary": "", "title": None},
            )

        # detect content language
        detected_language = self._identify_language(str(content))
        logger.debug(f"Detected content language: {detected_language}")

        if (
            payload.parameters.input_language is None
            or LanguageIso.from_language_iso(payload.parameters.input_language) is None
        ):
            input_language = detected_language
        else:
            input_language = LanguageIso.from_language_iso(
                payload.parameters.input_language
            )

        if detected_language != input_language:
            content = self._translate(
                content=content,
                input_language=detected_language,
                output_language=input_language,
            )

        # check if output_language is provided
        if (
            payload.parameters.output_language is None
            or LanguageIso.from_language_iso(payload.parameters.output_language) is None
        ):
            output_language = input_language
        else:
            output_language = LanguageIso.from_language_iso(
                payload.parameters.output_language
            )

        # retrieve prompt
        # depending on request parameters, we can determine what prompt to use.
        if parameters.summary_type not in settings.supported_summary_types:
            raise SummaryTypeNotSupportedException(summary_type=parameters.summary_type)

        try:
            prompt_alias = self._retrieve_prompt_alias(
                input_language=input_language,
                summary_type=parameters.summary_type,
                multiple_article_summary=multiple_article_summary,
            )
        except Exception as e:
            logger.error(f"Summarization input language {input_language} is invalid.")
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

        result = self._inference(
            content=content,
            desired_length=parameters.desired_length,
            keywords=parameters.keywords,
            title=parameters.title,
            theme=parameters.theme,
            custom_instructions=parameters.custom_instructions,
            prompt_alias=prompt_alias,
        )

        title = result.get("title", None)
        summary = result.get("summary")

        if title is not None:
            title = re.sub("\n+", " ", title)

        summary = re.sub("\n+", " ", summary)

        if input_language not in LanguageIso or input_language != output_language:
            summary = self._translate(
                content=summary,
                input_language=input_language,
                output_language=output_language,
            )
            if title is not None:
                title = self._translate(
                    content=title,
                    input_language=input_language,
                    output_language=output_language,
                )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"summary": summary, "title": title},
        )
