"""Sentiment v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseModel
from onclusiveml.core.serialization import JsonApiSchema


class InputEntity(OnclusiveBaseModel):
    """Input entity information from sentiment result.

    Attributes:
        entity_type (Optional[str]): The type of the extracted entity.
        entity_text (str): The text of the extracted entity
        score (Optional[float]): Confidence score of extracted entity
        sentence_index (Optional[int]): Index of the sentence containing the entity
        start (Optiona[int]): Start position of entity in the sentence
        end (Optiona[int]): End position of entity in the sentence
    """

    entity_type: Optional[str] = None
    entity_text: str
    score: Optional[float] = None
    sentence_index: Optional[int] = None
    start: Optional[int] = None
    end: Optional[int] = None


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        content (str):
        entities (Optional[List[InputEntity]]):
                List of detected entities from the sentiment model
    """

    content: str = ""
    entities: Optional[List[InputEntity]] = None


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data.

    Attributes:
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    language: str = "en"


class OutputEntity(InputEntity):
    """Input entity information from sentiment result.

    Attributes:
        sentiment: str
    """

    sentiment: str


class PredictResponseAttributeSchemaV1(JsonApiSchema):
    """Prediction request data.

    Attributes:
        label (str): Overall sentiment of the article
        negative_prob (float): Probablity of negative sentiment
        positive_prob (float): Probablity of positive sentiment
        entities (Optional[List[OutputEntity]]): entities with detected sentiment
    """

    label: str
    negative_prob: float
    positive_prob: float
    entities: Optional[List[OutputEntity]] = None


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "sentiment"
    model_card: Dict
