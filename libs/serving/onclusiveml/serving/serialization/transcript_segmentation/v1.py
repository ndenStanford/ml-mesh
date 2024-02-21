"""Transcript Segmentation v1 data schemas."""

# Standard Library
from typing import List, Optional, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    transcript: list
    keywords: List[str]


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction response data."""

    start_time: Union[float, int]
    end_time: Union[float, int]
    transcript_start_time: Union[float, int]
    transcript_end_time: Union[float, int]
    title: Optional[str] = None
    summary: Optional[str] = None
    ad: Optional[str] = None


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "transcript-segmentation"
