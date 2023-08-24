# Standard Library
from typing import List

# 3rd party libraries
from pydantic import BaseModel


class EntityOutputNoPos(BaseModel):
    """
    Output info of an entity without position

    Attributes:
        entity_type (str): The recognized entity's name
        score (float): confidence score for entity
        entity_text (str): Text representing entity
    """

    entity_type: str
    score: float
    entity_text: str


class EntityOutput(EntityOutputNoPos):
    """
    Output info of an entity with position

    Attributes:
        start (int): The starting position of the text in the input text
        end (int): The ending position of the text in the input text
    """

    start: int
    end: int


class InferenceOutput(BaseModel):
    """
    Output of the NER inference process

    Attributes:
        ner_labels (List[List[EntityOutput]]): List of list containing entity ouputs.
            Each inner list corresponds to a sentence.
    """

    ner_labels: List[List[EntityOutput]]


class PostprocessOutput(EntityOutput):
    """
    Post processed output info  of an entity with position info

    Attributes:
        sentence_index (int): The index of the sentence containing the entity
    """

    sentence_index: int


class PostprocessOutputNoPos(EntityOutputNoPos):
    """
    Post processed output info of an entity without position info

    Attributes:
        sentence_index (int): The index of the sentence containing the entity
    """

    sentence_index: int
