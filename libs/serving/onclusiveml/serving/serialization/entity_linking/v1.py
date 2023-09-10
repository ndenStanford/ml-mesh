"""Entity linking v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchema(JsonApiSchema):
    """Prediction request data."""

    content: str


class PredictRequestParametersSchema(JsonApiSchema):
    """Prediction request paramaters data."""

    lang: str = "en"


class PredictResponseEntity(JsonApiSchema):
    """Prediction entity."""

    entity_type: Optional[str] = None
    entity_text: Optional[str] = None
    score: Optional[str] = None
    sentence_index: Optional[str] = None
    wiki_link: Optional[str] = None


class PredictResponseAttributeSchema(JsonApiSchema):
    """Prediction request data."""

    entities: List[PredictResponseEntity] = []


class BioRequestAttributeSchema(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (Dict): Information about the model
    """

    model_name: str
