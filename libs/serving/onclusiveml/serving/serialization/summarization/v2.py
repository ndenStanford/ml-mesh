"""Summarization v2 data schemas."""

# Standard Library
from typing import Dict, List, Optional, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV2(JsonApiSchema):
    """Prediction request data.

    Attributes:
        content (Union[str, List]): Content for prediction, which can be a string or a list or articles.
    """

    content: Union[str, List] = ""


class PredictRequestParametersSchemaV2(JsonApiSchema):
    """Prediction request paramaters data.

    Attributes:
        desired_length (int): Desired token length of summary used in the prompt
    """

    input_language: Optional[str] = None
    output_language: Optional[str] = None
    summary_type: str = "bespoke"
    theme: Optional[str] = None
    keywords: List[str] = []
    title: Optional[bool] = False
    desired_length: int = 100
    custom_instructions: Optional[List] = None


class PredictResponseAttributeSchemaV2(JsonApiSchema):
    """Prediction request data.

    Attributes:
        summary (str): Summary text in string
    """

    summary: str
    title: str


class BioRequestAttributeSchemaV2(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "summarization"
    model_card: Dict
