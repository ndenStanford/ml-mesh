"""Translation handler."""

# Standard Library
import re
from typing import Any, Dict, List, Optional, Type

# 3rd party libraries
import boto3

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.language import constants, detect_language, filter_language
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()
logger = get_default_logger(__name__)


class TranslationModel(ServedModel):
    """Translation handler."""

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def __init__(self) -> None:
        self.sentence_tokenizer = SentenceTokenizer()
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

    def _chunk_content(self, content: str, max_length: int, language: str) -> List[str]:
        """Split the content into chunks, breaking only at sentence boundaries."""
        sentences = self.sentence_tokenizer.tokenize(
            content=content, language=language
        )["sentences"]
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) < max_length:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())

        return [i for i in chunks if len(i) > 0]

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Prediction."""
        attributes = payload.data.attributes
        parameters = payload.data.parameters

        content = attributes.content
        target_language = parameters.target_language
        # reference language will serve as the provided language, source_language os the detected language # noqa
        source_language = reference_language = parameters.source_language
        translation = parameters.translation
        # Raise error if the content is an empty string
        if not content.strip():
            raise ValueError("Input content cannot be an empty string.")

        content = self.pre_process(content)
        # Detect language from the first 500 characters
        language_detection_content = content[:500]

        if reference_language:
            try:
                # Convert the provided language to ISO value
                reference_language = constants.LanguageIso.from_locale_and_language_iso(
                    reference_language
                ).value
            except Exception:
                reference_language = None

        try:
            iso_language = self._detect_language(
                content=language_detection_content, language=None
            )
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
            if reference_language != source_language:
                # Log warning if detected language is different from provided language
                logger.warning(
                    f"Source language does not match detected language: '{source_language}'. Overriding with detected language."  # noqa
                )
            # Split content into chunks if longer than 8000 characters, break at sentence boundaries # noqa
            if len(content) > 5000:
                content_chunks = self._chunk_content(
                    content, max_length=5000, language=source_language
                )
            else:
                content_chunks = [content]

            try:
                # Translate each chunk and concatenate the results
                translated_chunks = []
                for chunk in content_chunks:
                    output = self._predict(
                        content=chunk,
                        language=source_language,
                        target_language=target_language,
                    )
                    translated_chunks.append(output)
                translated_text = " ".join(
                    translated_chunks
                )  # Join all translated chunks
            except (
                LanguageDetectionException,
                LanguageFilterException,
            ) as language_exception:
                raise OnclusiveHTTPException(
                    status_code=204, detail=language_exception.message
                )

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

    @property
    def client(self) -> Any:
        """Setup boto3 session."""
        boto3.setup_default_session(
            profile_name=settings.aws_profile,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
        return boto3.client(
            service_name=settings.service_name,
            region_name=settings.region_name,
        )

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
            response = self.client.translate_text(
                Text=content,
                SourceLanguageCode=language,
                TargetLanguageCode=target_language,
                Settings={
                    "Profanity": settings.profanity,
                },
            )
            return response["TranslatedText"]
        else:
            raise OnclusiveHTTPException(
                status_code=204,
                detail="Article too long",
            )
