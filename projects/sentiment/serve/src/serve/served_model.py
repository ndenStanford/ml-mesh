"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.sentiment import CompiledSent
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.params import ServedModelArtifacts
# from src.serve.server_models import (
#     BioResponseSchema,
#     PredictionOutputContent,
#     PredictRequestSchema,
#     PredictResponseSchema,
# )
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)


class ServedSentModel(ServedModel):
    """Served Sent model.

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

        super().__init__(name=served_model_artifacts.model_name)

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledSent instance
        self.model = CompiledSent.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded Sent model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing extracted entities
        """
        # content and configuration from payload
        configuration = payload.configuration
        inputs = payload.inputs
        # score the model
        sentiment = self.model.extract_sentiment(
            sentences=inputs.content, **configuration.dict()
        )

        sentiment_model = PredictionOutputContent(
            label=sentiment.get("label"),
            negative_prob=sentiment.get("negative_prob"),
            positive_prob=sentiment.get("positive_prob"),
            entities=sentiment.get("entities"),
        )

        return PredictResponseSchema(outputs=sentiment_model)

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served Sent model.

        Returns:
            BioResponseSchema: Bio information about the model
        """
        return BioResponseSchema(model_name=self.name, model_card=self.model_card)
