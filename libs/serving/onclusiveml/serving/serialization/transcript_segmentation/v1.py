"""Transcript Segmentation v1 data schemas."""

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    transcript: list
    keyword: str


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    segmented_transcript: list
    output_truncated: bool
    input_truncated: bool


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "transcript-segmentation"
