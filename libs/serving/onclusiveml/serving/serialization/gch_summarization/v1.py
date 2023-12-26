"""GCH Summarization v1 data schemas."""

# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str = ""


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    language: str = "en"


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    summary: str


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "gch-summarization"
    model_card: Dict
