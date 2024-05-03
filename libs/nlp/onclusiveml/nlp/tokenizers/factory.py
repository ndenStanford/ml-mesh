"""Base Tokenize Factory."""

# Standard Library
from typing import Dict

# Internal libraries
from onclusiveml.nlp.tokenizers.base_tokenizer import BaseTokenizer


class TokenizerFactory:
    """Factory class to retrieve a tokenizer given an index."""

    def __init__(self) -> None:
        """Initialize factory class."""
        self._creators: Dict = {}

    def register_language(self, language: str, tokenizer: BaseTokenizer) -> None:
        """Initialize tokenizer."""
        self._creators[language] = tokenizer

    def get_tokenizer(self, language: str) -> None:
        """Retrieve tokenizer."""
        creator = self._creators.get(language)
        if not creator:
            raise ValueError(language)
        return creator
