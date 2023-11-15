"""IPTC v1 data schemas."""

# Standard Library
from typing import Dict

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


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        label (str): Overall iptc of the article
        score (float): Probablity of iptc
    """

    label: str
    score: float


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "iptc"
    model_card: Dict
