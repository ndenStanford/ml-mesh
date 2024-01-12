"""Topic Summarization v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: List[str]


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    topic: Optional[Dict[str, Optional[Union[str, Dict[str, str]]]]]


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "topic-summarization"
