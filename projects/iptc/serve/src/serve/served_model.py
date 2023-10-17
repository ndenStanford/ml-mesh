"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.iptc import CompiledIPTC
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.params import ServedModelArtifacts
from src.serve.server_models import (
    BioResponseModel,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)


class ServedIPTCModel(ServedModel):
    """Served IPTC model.

    Attributes:
        predict_request_model (Type[BaseModel]):  Request model for prediction
        predict_response_model (Type[BaseModel]): Response model for prediction
        bio_response_model (Type[BaseModel]): Response model for bio
    """

    predict_request_model: Type[BaseModel] = PredictRequestModel
    predict_response_model: Type[BaseModel] = PredictResponseModel
    bio_response_model: Type[BaseModel] = BioResponseModel

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served IPTC model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts

        super().__init__(name=served_model_artifacts.model_name)

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledIPTC instance
        self.model = CompiledIPTC.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestModel) -> PredictResponseModel:
        """Make predictions using the loaded IPTC model.

        Args:
            payload (PredictRequestModel): The input data for making predictions

        Returns:
            PredictResponseModel: Response containing extracted entities
        """
        # content and configuration from payload
        configuration = payload.configuration
        inputs = payload.inputs
        # score the model
        iptc = self.model.extract_iptc(
            input_data=inputs.content, **configuration.dict()
        )

        iptc_model = PredictionOutputContent(
            label=iptc.get("label"),
            score=iptc.get("score"),
        )

        return PredictResponseModel(outputs=iptc_model)

    def bio(self) -> BioResponseModel:
        """Get bio information about the served IPTC model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseModel(model_name=self.name, model_card=self.model_card)
