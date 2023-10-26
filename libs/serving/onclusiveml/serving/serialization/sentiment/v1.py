"""Ner v1 data schemas."""

# Standard Library
from typing import Dict, List, Optional, Union

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema


class PredictRequestAttributeSchemaV1(JsonApiSchema):
    """Prediction request data."""

    content: str = ""

class InputEntity(JsonApiSchema):
    """Input entity information from NER result.

    Attributes:
        entity_type (Optional[str]): The type of the extracted entity.
        text (str): The text of the extracted entity
        score (Optional[float]): Confidence score of extracted entity
        sentence_index (Optional[int]): Index of the sentence containing the entity
        start (Optiona[int]): Start position of entity in the sentence
        end (Optiona[int]): End position of entity in the sentence
    """

    entity_type: Optional[str]
    text: str
    score: Optional[float]
    sentence_index: Optional[int]
    start: Optional[int]
    end: Optional[int]


class PredictRequestParametersSchemaV1(JsonApiSchema):
    """Prediction request paramaters data.
    
    Attributes:
        entities (Optional[List[InputEntity]]):
                List of detected entities from the NER model
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    entities: Optional[List[InputEntity]]
    language: str = "en"


class OutputEntity(InputEntity):
    """Input entity information from NER result.

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
    entities: Optional[List[OutputEntity]]


class BioRequestAttributeSchemaV1(JsonApiSchema):
    """Response model for a bio response.

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "ner"
    model_card: Dict
