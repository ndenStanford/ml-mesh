"""Sentence Tokenize."""

# Standard Library
import re
import ssl
import subprocess
from typing import Any, Dict, List

# 3rd party libraries
import nltk
import spacy
from konoha import SentenceTokenizer as konoha_tokenize

# Internal libraries
from onclusiveml.nlp.tokenizers.sentence.src.zh_sentence import (
    tokenize as zh_tokenize,
)


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
# Download nltk tokenizers and Spacy tokenizer for Korean
nltk.download("punkt")
nltk.download("punkt_tab")
command = "python -m spacy download ko_core_news_sm"
subprocess.run(command, shell=True, check=True)

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.sentence.base_tokenizer import (
    BaseSentenceTokenizer,
)


class NLTKSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing sentences in a given text."""

    def __init__(self) -> None:
        self.regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Uses both nltk sentence tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "english")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        try:
            sentences_first = nltk.sent_tokenize(content, language)
        except LookupError:
            # Fallback to the default tokenizer if the specific language is not found
            print(
                f"Warning: Language model for '{language}' not found. Falling back to default."
            )
            sentences_first = nltk.sent_tokenize(content)

        sentences = []
        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret


class ZhSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Chinese sentences in a given text."""

    # chinese specific tokenizer
    def tokenize(self, content: str, language: str = "chinese") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "chinese")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        sentences = zh_tokenize(content)
        ret = {"sentences": sentences}

        return ret


class SpacySentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Korean sentences in a given text."""

    def __init__(self) -> None:
        """Initialize and load the Spacy models for each language."""
        self.language_to_spacy_model = {
            "korean": "ko_core_news_sm",  # Korean
        }
        self.nlp = {}
        for language, model_name in self.language_to_spacy_model.items():
            self.nlp[language] = spacy.load(model_name)

    def tokenize(self, content: str, language: str = "korean") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "korean")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        doc = self.nlp[language](content)
        sentences = [sent.text for sent in doc.sents]
        ret = {"sentences": sentences}

        return ret


class KonohaSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Japanese sentences in a given text."""

    def __init__(self) -> None:
        self.tokenizer = konoha_tokenize()

    # chinese specific tokenizer
    def tokenize(
        self, content: str, language: str = "japanese"
    ) -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "japanese")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        sentences = self.tokenizer.tokenize(content)
        ret = {"sentences": sentences}

        return ret
