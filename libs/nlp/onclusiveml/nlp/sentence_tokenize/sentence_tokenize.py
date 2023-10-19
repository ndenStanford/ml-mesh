"""Sentence Tokenize."""

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk

# Internal libraries
from onclusiveml.core.logging import get_default_logger


nltk.download("punkt")
logger = get_default_logger(__name__)

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.sentence_tokenize.consts import (
    NLTK_SUPPORTED_LANGS,
    SPECIAL_CHARACTERS,
)


class SentenceTokenizer:
    """Tokenizing sentences in a given text."""

    regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

    def tokenize(self, content: str, language: str = "en") -> Dict[str, List[Any]]:
        """Tokenizes the input content into sentences.

        Uses both nltk sentence tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default to "en")

        Returns:
            dict: Dictionary containing tokenized setences
        """
        # return language iso equivalent of language e.g. fr is LanguageIso.FR
        langIso = LanguageIso.from_language_iso(language)

        # if LanguageIso of the language is not None, return english name of LanguageIso
        # e.g. LanguageIso.FR is french
        if langIso:
            lang_simplified = next(iter(langIso.locales.values()))["en"].lower()
        else:
            lang_simplified = "english"

        if lang_simplified in NLTK_SUPPORTED_LANGS:
            sentences_first = nltk.sent_tokenize(content, lang_simplified)
        else:
            sentences_first = nltk.sent_tokenize(content, "english")

        sentences = []
        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret
