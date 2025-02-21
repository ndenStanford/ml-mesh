"""Prediction model."""

# Standard Library
from typing import Type

# 3rd party libraries
from fastapi import HTTPException, status

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.serving.rest.serve import ServedModel

# Source
from src.serve.exceptions import (
    PromptBackendException,
    StructuredOutputException,
)
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

    predict_request_model: Type[OnclusiveBaseModel] = PredictRequestSchema
    predict_response_model: Type[OnclusiveBaseModel] = PredictResponseSchema
    bio_response_model: Type[OnclusiveBaseModel] = BioResponseSchema

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
        parameter_input = payload.parameters

        try:
            (
                (start_time_offsetted, end_time_offsetted),
                (start_time, end_time),
                title,
                summary,
                segment,
                ad_detect_output,
            ) = self.model.__call__(
                word_transcript=inputs.transcript,
                keywords=inputs.keywords,
                country=parameter_input.country,
                offset_start_buffer=parameter_input.offset_start_buffer,
                offset_end_buffer=parameter_input.offset_end_buffer,
            )
        except PromptBackendException as e:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e),
            )
        except StructuredOutputException as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )

        return PredictResponseSchema.from_data(
            version=int(settings.api_version[1:]),
            namespace=settings.model_name,
            attributes={
                "start_time": start_time,
                "end_time": end_time,
                "transcript_start_time": start_time_offsetted,
                "transcript_end_time": end_time_offsetted,
                "title": title,
                "summary": summary,
                "ad": ad_detect_output,
                "segment": segment,
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
