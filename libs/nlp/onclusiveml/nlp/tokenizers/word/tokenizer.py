"""Word tokenizer."""

# Standard Library
import re
import ssl
import subprocess
from typing import Any, Dict, List

# 3rd party libraries
import jieba
import nltk
import spacy
from konoha import WordTokenizer


# skip cert verification
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt_tab")
command = "python -m spacy download ko_core_news_sm"
subprocess.run(command, shell=True, check=True)

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.word.base_tokenizer import BaseWordTokenizer


class NLTKWordTokenizer(BaseWordTokenizer):
    """Tokenizing words in a given text."""

    def __init__(self) -> None:
        self.regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized words
        """
        words_first = nltk.word_tokenize(content, language)
        words = []

        for word in words_first:
            w = self.regex.split(word)
            words += w

        ret = {"words": words}

        return ret


class JiebaWordTokenizer(BaseWordTokenizer):
    """Tokenizing Chinese words in a given text."""

    def tokenize(self, content: str, language: str = "chinese") -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text

        Returns:
            dict: Dictionary containing tokenized words
        """
        words = jieba.lcut(content)

        ret = {"words": words}

        return ret


class SpacyWordTokenizer(BaseWordTokenizer):
    """Tokenizing Korean words in a given text."""

    def __init__(self) -> None:
        """Initialize and load the Spacy models for each language."""
        self.language_to_spacy_model = {
            "korean": "ko_core_news_sm",  # Korean
        }
        self.nlp = {}
        for language, model_name in self.language_to_spacy_model.items():
            self.nlp[language] = spacy.load(model_name)

    def tokenize(self, content: str, language: str = "korean") -> Dict[str, List[Any]]:
        """Tokenizes the input content into words using SpaCy.

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text

        Returns:
            dict: Dictionary containing tokenized words
        """
        # Process the content using SpaCy
        doc = self.nlp[language](content)
        # Extract the words from the SpaCy doc
        words = [token.text for token in doc if not token.is_space]

        return {"words": words}


class KonohaWordTokenizer(BaseWordTokenizer):
    """Tokenizing Japanese words in a given text."""

    def __init__(self) -> None:
        self.tokenizer = WordTokenizer("Janome")

    def tokenize(
        self, content: str, language: str = "japanese"
    ) -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text

        Returns:
            dict: Dictionary containing tokenized words
        """
        tokens = self.tokenizer.tokenize(content)
        words = [str(token.surface) for token in tokens]
        ret = {"words": words}

        return ret
