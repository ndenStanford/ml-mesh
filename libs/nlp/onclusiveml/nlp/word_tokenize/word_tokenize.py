# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk


nltk.download("punkt")

# Internal libraries
from onclusiveml.nlp.sentence_tokenize.consts import SPECIAL_CHARACTERS


class WordTokenizer:
    """Tokenizing words in a given text."""

    regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:
        """
        Tokenizes the input content into words.
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
