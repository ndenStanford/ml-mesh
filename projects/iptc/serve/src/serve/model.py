"""Prediction model."""

# Standard Library
from typing import Type

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.models.iptc import CompiledIPTC
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


class ServedIPTCModel(ServedModel):
    """Served IPTC model.

    Attributes:
        predict_request_model (Type[OnclusiveBaseModel]):  Request model for prediction
        predict_response_model (Type[OnclusiveBaseModel]): Response model for prediction
        bio_response_model (Type[OnclusiveBaseModel]): Response model for bio
    """

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

    def __init__(self, served_model_artifacts: ServedModelArtifacts):
        """Initalize the served IPTC model with its artifacts.

        Args:
            served_model_artifacts (ServedModelArtifacts): Served model artifact
        """
        self.served_model_artifacts = served_model_artifacts
        self._model = None
        super().__init__(name=served_model_artifacts.model_name)
        # self.load()  # FOR LOCAL TESTING ONLY, REMOVE FOR PRODUCTION

    @property
    def model(self) -> CompiledIPTC:
        """Model class."""
        if self.ready:
            return self._model
        raise ValueError(
            "Model has not been initialized. Please call .load() before making a prediction"
        )

    def load(self) -> None:
        """Load the model artifacts and prepare the model for prediction."""
        # load model artifacts into ready CompiledIPTC instance
        self._model = CompiledIPTC.from_pretrained(
            settings.project, self.served_model_artifacts.model_artifact_directory
        )
        # load model card json file into dict
        self.model_card = self.served_model_artifacts.model_card
        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Make predictions using the loaded IPTC model.

        Args:
            payload (PredictRequestSchema): The input data for making predictions

        Returns:
            PredictResponseSchema: Response containing extracted entities
        """
        # attributes and parameters from payload
        attributes = payload.attributes
        parameters = payload.parameters

        if attributes.content == "":
            iptc_list: list = []
        else:
            # score the model
            iptc_list = self.model(
                input_data=attributes.content, **parameters.model_dump()
            )
        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"iptc": [iptc.model_dump() for iptc in iptc_list]},
        )

    def bio(self) -> BioResponseSchema:
        """Get bio information about the served iptc model.

        Returns:
            BioResponseModel: Bio information about the model
        """
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=self.name,
            attributes={"model_name": self.name, "model_card": self.model_card},
        )
