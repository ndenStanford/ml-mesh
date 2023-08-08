# Standard Library
from typing import List

# 3rd party libraries
from pydantic import BaseModel


class EntityOutputNoPos(BaseModel):
    entity: str
    score: float
    word: str


class EntityOutput(EntityOutputNoPos):
    start: int
    end: int


class InferenceOutput(BaseModel):
    ner_labels: List[List[EntityOutput]]


class PostprocessOutput(EntityOutput):
    sentence_index: int


class PostprocessOutputNoPos(EntityOutputNoPos):
    sentence_index: int
