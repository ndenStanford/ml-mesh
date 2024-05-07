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
    """Prediction request paramaters data."""

    language: str = "en"
    target_language: str = "en"
    desired_length: Optional[int] = 100
    max_tokens: Optional[int] = 512
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 1
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0


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

    model_name: str = "gpt-3.5-turbo"
    model_card: Dict
