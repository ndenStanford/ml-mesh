# isort: skip_file
# black:skip_file
"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.schema import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.serve._init import get_settings

from src.serve.topic import TopicHandler

settings = get_settings()


class ServedTopicModel(ServedModel):
    """Served Topic detection model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="topic-summarization")

    def load(self) -> None:
        """Load model."""
        # load model artifacts into ready CompiledKeyBERT instance
        self.model = TopicHandler()
        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Topic-detection prediction.

        Args:
            payload (PredictRequestModel): prediction request payload.
        """
        # extract inputs data and inference specs from incoming payload
        inputs = payload.attributes
        content = inputs.content

        topic = self.model.aggregate(content)

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "topic": topic,
            },
        )

    def bio(self) -> BioResponseSchema:
        """Model bio endpoint."""
        return BioResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={"model_name": settings.model_name},
        )
