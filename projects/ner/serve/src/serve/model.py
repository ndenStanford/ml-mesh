"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.models.ner import CompiledNER
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


class ServedNERModel(ServedModel):
    """Served NER model.

    Attributes:
        predict_request_model (Type[BaseModel]):  Request model for prediction
        predict_response_model (Type[BaseModel]): Response model for prediction
        bio_response_model (Type[BaseModel]): Response model for bio
    """

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served NER model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)

    @property
    def model(self) -> CompiledNER:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledNER instance
        self._model = CompiledNER.from_pretrained(
            self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card

        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded NER model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing extracted entities
        """
        # attributes and parameters from payload
        attributes = payload.attributes
        parameters = payload.parameters

        if attributes.content == "":
            entities: list = [[]]
        else:
            # score the model
            entities = self.model(sentences=[attributes.content], **parameters.dict())

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"entities": [entity._asdict() for entity in entities[0]]},
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served NER model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema(model_name=self.name, model_card=self.model_card)
