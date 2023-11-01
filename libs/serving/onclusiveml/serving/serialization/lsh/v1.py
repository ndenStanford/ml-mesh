"""Ner v1 data schemas."""

# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str = ""


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    language: str = "en"
    shingle_list: int = 5
    threshold: float = 0.6
    num_perm: int = 128


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    signature: Optional[List[str]]


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "lsh"
