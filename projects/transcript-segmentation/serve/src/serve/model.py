"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.handler import TranscriptSegmentationHandler
from src.serve.schemas import (
    BioResponseSchema,
    PredictRequestSchema,
    PredictResponseSchema,
)
from src.settings import get_settings


settings = get_settings()


class ServedTranscriptSegmentationModel(ServedModel):
    """Served Transcript Segmentation model."""

    predict_request_model: Type[BaseModel] = PredictRequestSchema
    predict_response_model: Type[BaseModel] = PredictResponseSchema
    bio_response_model: Type[BaseModel] = BioResponseSchema

    def __init__(self) -> None:
        super().__init__(name="transcript-segmentation")

    def load(self) -> None:
        """Load Handler."""
        # Instantiate handler class
        self.model = TranscriptSegmentationHandler()
        self.ready = True

    def predict(self, payload: PredictRequestSchema) -> PredictResponseSchema:
        """Transcript Segmentation prediction.

        Args:
            payload (PredictRequestModel): prediction request payload.
        """
        # extract inputs data and inference specs from incoming payload
        inputs = payload.attributes

        (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            title,
        ) = self.model.__call__(
            word_transcript=inputs.transcript, keywords=inputs.keywords
        )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "start_time": start_time_offsetted,
                "end_time": end_time_offsetted,
                "transcript_start_time": start_time,
                "transcript_end_time": end_time,
                "title": title,
                "ad": None,
            },
        )

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
