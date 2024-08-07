"""Summarization v1 data schemas."""

# Standard Library
from typing import Dict, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        content (str):
    """

    content: str = ""


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data.

    Attributes:
        desired_length (int): Desired token length of summary used in the prompt
    """

    language: str = "en"
    target_language: str = "en"
    desired_length: Optional[int] = 100


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        summary (str): Summary text in string
    """

    summary: str


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "summarization"
    model_card: Dict
