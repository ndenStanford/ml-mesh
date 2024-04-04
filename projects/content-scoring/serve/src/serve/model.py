"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
import pandas as pd
from pydantic import BaseModel
from sklearn.preprocessing import OrdinalEncoder

# Internal libraries
from onclusiveml.models.content_scoring import CompiledContentScoring
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.artifacts import ServedModelArtifacts
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class ServedContentScoringModel(ServedModel):
    """Served Content Scoring model.

    Attributes:
        predict_request_model (Type[BaseModel]):  Request model for prediction
        predict_response_model (Type[BaseModel]): Response model for prediction
        bio_response_model (Type[BaseModel]): Response model for bio
    """

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initialize the served Content Scoring model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)

    @property
    def model(self) -> CompiledContentScoring:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # Load model artifacts into ready CompiledContentScoring instance
        content_model_directory = self.served_model_artifacts.model_artifact_directory
        ordinal_encoder = OrdinalEncoder()
        self._model = CompiledContentScoring.from_pretrained(
            content_model_directory, ordinal_encoder
        )
        # Load model card JSON file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded Content Scoring model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing content scores
        """
        print("payload input: ", payload)
        df = pd.DataFrame(payload)
        content_status = self.model(df)

        response_data = {"messages": content_status}

        print("response data: ", response_data)

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes=response_data,
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served Content Scoring model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=self.name,
            attributes={"model_name": self.name, "model_card": self.model_card},
        )
