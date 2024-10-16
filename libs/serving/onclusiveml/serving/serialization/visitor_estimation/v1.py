"""Visitor estimation v1 data schemas."""

# Standard Library
from typing import Dict, List

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        input (List[dict]): Input dictionary.
    """

    input: List[dict]


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data.

    Attributes:
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    language: str = "en"


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction response data."""

    predicted_visitors: float


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "visitor-estimation"
    model_card: Dict
