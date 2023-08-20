# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.sentiment import CompiledSent
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.server_models import (
    BioResponseModel,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)
from src.serving_params import ServedModelArtifacts


class ServedSentModel(ServedModel):
    """
    Served Sent model

    Attributes:
        predict_request_model (Type[BaseModel]):  Request model for prediction
        predict_response_model (Type[BaseModel]): Response model for prediction
        bio_response_model (Type[BaseModel]): Response model for bio
    """

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """
        Initalize the served Sent model with its artifacts

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts

        super().__init__(name=served_model_artifacts.model_name)

    def load(self) -> None:
        """
        Load the model artifacts and prepare the model for prediction
        """
        # load model artifacts into ready CompiledSent instance
        self.model = CompiledSent.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )

        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        """
        Make predictions using the loaded Sent model

        Args:
            payload (PredictRequestModel): The input data for making predictions

        Returns:
            PredictResponseModel: Response containing extracted entities
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

        return PredictResponseModel(outputs=sentiment_model)

    def bio(self) -> BioResponseModel:
        """
        Get bio information about the served Sent model

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseModel(model_name=self.name, model_card=self.model_card)
