"""Translation handler."""

# Standard Library
import re
from typing import Any, Dict, Optional, Type

# 3rd party libraries
import boto3
from pydantic import BaseModel

# Internal libraries
from onclusiveml.nlp.language import detect_language, filter_language
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class TranslationModel(ServedModel):
    """Translation handler."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="translation")

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": self.name},
        )

    def pre_process(self, text: str) -> str:
        """Pre process text."""
        text = re.sub("\n+", " ", text)
        return text

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        target_language = parameters.target_language
        source_language = parameters.source_language
        translation = parameters.translation

        content = self.pre_process(content)
        translated_text = None

        if not source_language:
            try:
                iso_language = self._detect_language(content=content, language=None)
                if iso_language:
                    source_language = iso_language.value
                else:
                    source_language = "Language not found"
            except LanguageDetectionException as language_exception:
                raise LanguageDetectionException(
                    status_code=204,
                    detail=language_exception.message,
                )

        if translation is True:
            try:
                output = self._predict(
                    content=content,
                    language=source_language,
                    target_language=target_language,
                )
            except (
                LanguageDetectionException,
                LanguageFilterException,
            ) as language_exception:
                raise OnclusiveHTTPException(
                    status_code=204, detail=language_exception.message
                )
            translated_text = output

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "source_language": source_language,
                "target_language": target_language,
                "translated_text": translated_text,
            },
        )

    def _detect_language(self, content: str, language: Optional[str]) -> LanguageIso:
        """Language detection."""
        return detect_language(content=content)

    @filter_language(
        supported_languages=list(LanguageIso),
        raise_if_none=True,
    )
    def _predict(
        self,
        content: str,
        language: str,
        target_language: str,
    ) -> Dict[str, Any]:
        """Language filtered prediction."""
        if len(content) < 10000:
            try:
                client = boto3.client(
                    service_name=settings.service_name,
                    region_name=settings.region_name,
                )
            except Exception as e:
                raise OnclusiveHTTPException(
                    status_code=204,
                    detail=e,
                )
            try:
                response = client.translate_text(
                    Text=content,
                    SourceLanguageCode=language,
                    TargetLanguageCode=target_language,
                    Settings={
                        "Profanity": settings.profanity,
                    },
                )

            except Exception as e:
                raise OnclusiveHTTPException(
                    status_code=204,
                    detail=e,
                )
            return response["TranslatedText"]
        else:
            raise OnclusiveHTTPException(
                status_code=204,
                detail="Article too long",
            )
