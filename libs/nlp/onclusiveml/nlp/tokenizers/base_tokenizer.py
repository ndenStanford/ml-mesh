"""Base Tokenize."""

# Standard Library
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseTokenizer(ABC):
    """Tokenizing sentences in a given text."""

    @abstractmethod
    def tokenize(self, content: str, language: Optional[str]) -> Dict[str, List[Any]]:
        """Tokenizes the input content.

        Args:
            content (str): Text to be tokenized
            language (str, optional): Language of the text to be tokenized

        Returns:
            dict: Dictionary containing tokens
        """
