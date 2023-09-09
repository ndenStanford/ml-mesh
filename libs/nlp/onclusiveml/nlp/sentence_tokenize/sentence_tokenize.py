"""Sentence Tokenize."""

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk


nltk.download("punkt")

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.sentence_tokenize.consts import SPECIAL_CHARACTERS


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
        # return english equivalent of LanguageIso e.g. LanguageIso.FR is french
        lang_simplified = next(iter(langIso.locales.values()))["en"].lower()

        sentences_first = nltk.sent_tokenize(content, lang_simplified)
        sentences = []

        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret
