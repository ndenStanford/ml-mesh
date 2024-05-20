"""Entity linking v1 data schemas."""

# Standard Library
from typing import List, Optional, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str
    entities: Optional[List[List[Optional[int]]]] = None
    mention_offsets: Optional[List[List[Optional[int]]]] = None
    mention_lengths: Optional[List[List[Optional[int]]]] = None


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data."""

    lang: str = "en"


class PredictResponseEntity(JsonApiSchema):
    """Prediction entity."""

    entity_text: Optional[str] = None
    score: Optional[float] = None
    sentence_index: Optional[Union[int, List[int]]] = None
    wiki_link: Optional[str] = None
    wiki_score: Optional[float] = None


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    entities: List[PredictResponseEntity] = []


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (Dict): Information about the model
    """

    model_name: str
