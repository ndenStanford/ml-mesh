"""Translation handler."""

# Standard Library
import re
from typing import Any, Dict, Type

# 3rd party libraries
import boto3
from pydantic import BaseModel

# Internal libraries
from onclusiveml.nlp.language import filter_language
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

    def bio(self) -> BioResponseSchema:
        """Model bio."""
        return BioResponseSchema.from_data(
            version=settings.api_version,
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
        target_language = attributes.target_lang
        original_language = parameters.lang
        brievety = parameters.brievety

        content = self.pre_process(content)

        try:
            output = self._predict(
                content=content,
                original_language=original_language,
                target_language=target_language,
                brievety=brievety,
            )
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=422, detail=language_exception.message
            )

        return PredictResponseSchema.from_data(
            version=settings.api_version,
            namespace=settings.model_name,
            attributes=output,
        )

    @filter_language(
        supported_languages=list(LanguageIso),
        raise_if_none=True,
    )
    def _predict(
        self,
        content: str,
        original_language: str,
        target_language: str,
        brievety: bool = False,
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
                    status_code=422,
                    detail=e,
                )
            if brievety:
                try:
                    response = client.translate_text(
                        Text=content,
                        SourceLanguageCode=original_language,
                        TargetLanguageCode=target_language,
                        Settings={
                            "Formality": settings.formallity,
                            "Profanity": settings.profanity,
                            "Brevity": "ON",
                        },
                    )
                except Exception as e:
                    raise OnclusiveHTTPException(
                        status_code=422,
                        detail=e,
                    )
            else:
                try:
                    response = client.translate_text(
                        Text=content,
                        SourceLanguageCode=original_language,
                        TargetLanguageCode=target_language,
                        Settings={
                            "Formality": settings.formallity,
                            "Profanity": settings.profanity,
                        },
                    )
                except Exception as e:
                    raise OnclusiveHTTPException(
                        status_code=422,
                        detail=e,
                    )
            return {"translation": response["TranslatedText"]}
        else:
            raise OnclusiveHTTPException(
                status_code=422,
                detail="Article too long",
            )
