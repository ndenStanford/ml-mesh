# Standard Library
from typing import Dict, List, Optional, Union

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """
    Configuration for prediction request

    Attributes:
        entities (Optional[List[Dict[str, Union[str, List]]]]):
                List of detected entities from the NER model
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    entities: Optional[List[Dict[str, Union[str, List]]]]
    language: Optional[str] = "en"


class PredictInputContentModel(BaseModel):
    """
    Input content for a prediction rerquest

    Attributes:
        content (str): The input content for prediction
    """

    content: str


class PredictRequestModel(BaseModel):
    """
    Request model for making a prediction

    Attributes:
        configuration (PredictConfiguration): The prediction configuration
        inputs (PredictInputContentModel): The input content for prediction
    """

    configuration: PredictConfiguration = PredictConfiguration()
    inputs: PredictInputContentModel


class InputEntity(BaseModel):
    """
    Input entity information from NER result

    Attributes:
        entity_type (str): The type of the extracted entity.
        text (str): The text of the extracted entity
        score (float): Confidence score of extracted entity
        sentence_index (int): Index of the sentence containing the entity
        start (Optiona[int]): Start position of entity in the sentence
        end (Optiona[int]): End position of entity in the sentence
    """

    entity_type: str
    text: str
    score: float
    sentence_index: int
    start: Optional[int] = None
    end: Optional[int] = None


class PredictionOutputContent(BaseModel):
    """
    Output content containing extracted entities from a prediction

    Attributes:
        label (str): Overall sentiment of the article
        negative_prob (float): Probablity of negative sentiment
        positive_prob (float): Probablity of positive sentiment
        entities (Optional[List[InputEntity]]): entities with detected sentiment
    """

    label: str
    negative_prob: float
    positive_prob: float
    entities: Optional[List[InputEntity]]


class PredictResponseModel(BaseModel):
    """
    Response model for a prediction request

    Attributes:
        output (PredictionOutputContent): The output content containing extracted entities
    """

    outputs: PredictionOutputContent


# --- bio response models
class BioResponseModel(BaseModel):
    """
    Response model for a bio response

    Attributes:
        model_name (str): The name of the model used for prediction
        model_card (Dict): Information about the model
    """

    model_name: str = "sentiment-model"
    model_card: Dict
