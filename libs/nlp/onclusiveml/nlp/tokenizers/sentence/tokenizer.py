"""Sentence Tokenize."""

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk
import spacy
from konoha import SentenceTokenizer as konoha_tokenize
from zh_sentence.tokenizer import tokenize as zh_tokenize


nltk.download("punkt")

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.sentence.base_tokenizer import (
    BaseSentenceTokenizer,
)


class NLTKSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing sentences in a given text."""

    regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

    def tokenize(self, content: str, language: str = "en") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Uses both nltk sentence tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "en")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        sentences_first = nltk.sent_tokenize(content, language)

        sentences = []
        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret


class ZhSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Chinese sentences in a given text."""

    # chinese specific tokenizer
    def tokenize(self, content: str, language: str = "zh") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        sentences = zh_tokenize(content)
        ret = {"sentences": sentences}

        return ret


class SpacySentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Korean sentences in a given text."""

    def __init__(
        self,
    ) -> None:
        """Define the Spacy model for each language."""
        self.language_to_spacy_model = {
            "english": "en_core_web_sm",
            "chinese": "zh_core_web_sm",
            "japanese": "ja_core_news_sm",
            "korean": "ko_core_news_sm",
        }

    def tokenize(self, content: str, language: str = "ko") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "ko")

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        language_model = self.language_to_spacy_model[language]
        nlp = spacy.load(language_model)
        doc = nlp(content)
        sentences = [sent.text for sent in doc.sents]
        ret = {"sentences": sentences}

        return ret


class KonohaSentenceTokenizer(BaseSentenceTokenizer):
    """Tokenizing Chinese sentences in a given text."""

    # chinese specific tokenizer
    def tokenize(self, content: str, language: str = "ja") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Args:
            content (str): Text to be tokenized into sentences

        Returns:
            dict: Dictionary containing tokenized sentences
        """
        tokenizer = konoha_tokenize()
        sentences = tokenizer.tokenize(content)
        ret = {"sentences": sentences}

        return ret
