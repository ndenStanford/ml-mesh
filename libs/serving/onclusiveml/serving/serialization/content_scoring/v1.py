"""Content scoring v1 data schemas."""

# Standard Library
from typing import Any, Dict, List

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    dataframe: Dict = {}


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        boolean_messages List(str): List of 'accepted' or 'rejected' corresponding to the prediction
    """

    boolean_messages: List[Any] = []


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "content-scoring"
    model_card: Dict
