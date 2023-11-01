"""Entity linking v1 data schemas."""

# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictResponseEntity(JsonApiSchema):
    """Prediction entity."""

    entity_type: Optional[str] = None
    entity_text: Optional[str] = None
    score: Optional[float] = None
    sentence_index: Optional[int] = None
    wiki_link: Optional[str] = None
    salience_score: Optional[float] = None
    text: Optional[str] = None


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str
    entities: Optional[List[PredictResponseEntity]] = None


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    lang: str = "en"


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    entities: List[PredictResponseEntity] = []


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (Dict): Information about the model
    """

    model_name: str
