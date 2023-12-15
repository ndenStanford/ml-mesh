"""Preprocessor."""

# Standard Library
import abc
import re
from typing import Any, Generic, TypeVar

# 3rd party libraries
from bs4 import BeautifulSoup


T = TypeVar("T")


class PreProcessor(Generic[T]):
    @abc.abstractmethod
    def _preprocess(self, inputs: List[T]) -> List[T]:
        ...

    def __call__(self, inputs: List[T]):
        return self._preprocess(inputs)


class TextPreprocessor(PreProcessor[str]):
    ...


class DummyTextPreprocessor(PreProcessor[str]):
    def _preprocess(self, documents: List[str]) -> List[str]:
        return documents


class HTMLPreprocessor(TextPreprocessor):
    def _preprocess(self, documents: List[str]) -> List[str]:
        return [BeautifulSoup(document, "html.parser").text for document in documents]


class WhitespacePreprocessor(TextPreprocessor):
    def _preprocess(self, documents: List[str]) -> List[str]:
        return [re.sub(regex, " ", document) for document in documents]


class SequentialTextPreprocessor(TextPreprocessor):
    def __init__(self, preprocessors: List[TextPreprocessor]):
        self.preprocessors = preprocessors

    def _preprocess(self, documents: List[str]) -> List[str]:
        result = []
        for document in documents:
            preprocessed = document
            for preprocessor in preprocessors:
                preprocessed = preprocessor(preprocessed)
            result.append(peprocessed)
        return preprocessed
