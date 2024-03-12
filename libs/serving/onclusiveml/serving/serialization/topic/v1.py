"""Topic v1 data schemas."""

# Standard Library
from typing import Dict, List

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        content (str):
                Input text.
    """

    content: str


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data.

    Attributes:
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    language: str = "en" #NOT NEEDED??


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction response data."""

    topic_id: str
    topic_representation: List[str]


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "topic"
    model_card: Dict
