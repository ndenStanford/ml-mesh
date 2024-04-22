"""Sentence Tokenize."""

# Standard Library
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class BaseSentenceTokenizer(ABC):
    """Tokenizing sentences in a given text."""

    @abstractmethod
    def tokenize(self, content: str, language: Optional[str]) -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences

        Returns:
            dict: Dictionary containing tokenized setences
        """
        pass
