"""Prediction model."""

# Standard Library
from typing import Any, Dict, List, Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.gch_summarization import TrainedSummarization
from onclusiveml.nlp.language import filter_language
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)
from onclusiveml.serving.rest.serve import OnclusiveHTTPException, ServedModel

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.constants import SAMPLE_INFERENCE
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class ServedSummarizationModel(ServedModel):
    """Served Summarization model.

    Attributes:
        predict_request_model (Type[BaseModel]):  Request model for prediction
        predict_response_model (Type[BaseModel]): Response model for prediction
        bio_response_model (Type[BaseModel]): Response model for bio
    """

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served Sent model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)
        # self.load()  # FOR LOCAL TESTING ONLY, REMOVE FOR PRODUCTION

    @property
    def model(self) -> TrainedSummarization:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledSent instance
        self._model = TrainedSummarization.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True
        self.sample_inference()

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded summarization model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing generated summarization prediction
        """
        # content and configuration from payload
        attributes = payload.attributes
        parameters = payload.parameters

        try:
            # score the model
            output = self._predict(
                content=attributes.content,
                language=parameters.language,
            )

            attributes = {
                "summary": output,
            }

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
            attributes=attributes,
        )

    @filter_language(
        supported_languages=settings.supported_languages,
        raise_if_none=True,
    )
    def _predict(self, content: str, language: str) -> List[List[Dict[str, Any]]]:
        """Generate text summary considering language and additional parameters.

        Args:
            content (str): The text content to summarize.
            language (str): The language of the text.

        Returns:
            summary (str): Generated summary.
        """
        return self.model(text=content, language=language)

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served Sentiment model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=self.name,
            attributes={"model_name": self.name, "model_card": self.model_card},
        )

    def sample_inference(self) -> None:
        """Make inference after model loading."""
        for lang, sample in SAMPLE_INFERENCE.items():
            self.model(text=sample, language=lang)
