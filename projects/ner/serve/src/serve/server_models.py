# Standard Library
from typing import Dict, List, Optional, Union

# 3rd party libraries
from pydantic import BaseModel


# --- prediction request models
class PredictConfiguration(BaseModel):
    """
    Configuration for prediction request

    Attributes:
        return_pos (Optional[bool]): Flag used to return position info or not. Defaults to True
        language (Optional[str]): Language used for prediction. Defaults to "en"
    """

    return_pos: Optional[bool] = True
    language: Optional[str] = "en"


class PredictInputContentModel(BaseModel):
    """
    Input ocntent for a prediction rerquest

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

    configuration: Optional[PredictConfiguration] = PredictConfiguration()
    inputs: PredictInputContentModel


class PredictionExtractedEntityNoPos(BaseModel):
    """
    Extracted entity information from a prediction without positional information

    Attributes:
        entity_type (str): The type of the extracted entity.
        entity_text (str): The text of the extracted entity
        score (float): Confidence score of extracted entity
        sentence_index (int): Index of the sentence containing the entity
    """

    entity_type: str
    entity_text: str
    score: float
    sentence_index: int


class PredictionExtractedEntity(PredictionExtractedEntityNoPos):
    """
    Extracted entity information from a prediction including positional information

    Attributes:
        start (Optiona[int]): Start position of entity in the sentence
        end (Optiona[int]): End position of entity in the sentence
    """

    start: int
    end: int


class PredictionOutputContent(BaseModel):
    """
    Output content containing extracted entities from a prediction

    Attributes:
        predicted_content (List[PredictionExtractedEntity]): List of extracted entities
    """

    predicted_content: Optional[
        Union[List[PredictionExtractedEntity], List[PredictionExtractedEntityNoPos]]
    ] = []


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

    model_name: str = "ner-model"
    model_card: Dict
