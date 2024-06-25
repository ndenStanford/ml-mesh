"""Prediction model."""

# Standard Library
from typing import List, Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.hashing.lsh import LshHandler
from onclusiveml.nlp.language import filter_language
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


class ServedLshModel(ServedModel):
    """Served LSH model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="lsh")

    def load(self) -> None:
        """Load model."""
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = LshHandler()
        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """LSH prediction.

        Args:
            payload (PredictRequestModel): prediction request payload.
        """
        # extract inputs data and inference specs from incoming payload
        inputs = payload.attributes
        configuration = payload.parameters

        try:
            words = self._predict(
                content=inputs.content, language=configuration.language
            )
        except (
            LanguageDetectionException,
            LanguageFilterException,
        ) as language_exception:
            raise OnclusiveHTTPException(
                status_code=204, detail=language_exception.message
            )

        shingle_list = self.model.k_shingle(words, k=configuration.shingle_list)
        if len(shingle_list) < 1:
            return PredictResponseSchema.from_data(
                version=int(settings.api_version[1:]),
                namespace=settings.model_name,
                attributes={"signature": None},
            )

        signature = self.model.generate_lsh_signature(
            shingle_list=shingle_list,
            num_perm=configuration.num_perm,
            threshold=configuration.threshold,
        )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"signature": signature},
        )

    @filter_language(
        supported_languages=settings.supported_languages,
        raise_if_none=True,
    )
    def _predict(self, content: str, language: str) -> List[str]:
        """Language filtering."""
        return self.model.pre_processing(text=content, lang=language)

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served Sentiment model.

        Returns:
            BioResponseSchema: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )
