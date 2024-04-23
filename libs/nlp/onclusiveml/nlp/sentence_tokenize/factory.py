"""Sentence Tokenize Factory."""

# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.nlp.sentence_tokenize.base_tokenizer import (
    BaseSentenceTokenizer,
)
from onclusiveml.nlp.sentence_tokenize.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.sentence_tokenize.nltk_tokenizer import (
    NLTKSentenceTokenizer,
)


class SentenceTokenizerFactory:
    """Factory class to retrieve a tokenizer given an index."""

    def __init__(self) -> None:
        """Initialize factory class."""
        self._creators: Dict = {}

    def register_language(
        self, language: str, sentence_tokenizer: BaseSentenceTokenizer
    ) -> None:
        """Initialize tokenizer."""
        self._creators[language] = sentence_tokenizer

    def get_sentence_tokenizer(self, language: str) -> None:
        """Retrieve tokenizer."""
        creator = self._creators.get(language)
        if not creator:
            raise ValueError(language)
        return creator


factory = SentenceTokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    factory.register_language(lang, NLTKSentenceTokenizer())
