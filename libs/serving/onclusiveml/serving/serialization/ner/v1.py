"""Ner v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str = ""


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    return_pos: bool = True
    language: str = "en"


class PredictResponseEntityV1(JsonApiSchema):
    """Prediction entity."""

    entity_type: Optional[str] = None
    entity_text: Optional[str] = None
    score: Optional[float] = None
    sentence_index: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    entities: List[PredictResponseEntity] = []


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "ner"
    model_card: Dict
