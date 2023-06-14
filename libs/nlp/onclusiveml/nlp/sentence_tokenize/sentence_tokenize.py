"Sentence Tokenize"

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk


nltk.download("punkt")

# Internal libraries
from onclusiveml.nlp.sentence_tokenize.consts import TOKENS


class SentenceTokenize:
    """Tokenizing sentences in a given text."""

    regex = re.compile(r"|".join(TOKENS))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:
        """
        Tokenizes the input content into sentences.
        Uses both nltk sentence tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into sentences
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized setences
        """

        sentences_first = nltk.sent_tokenize(content, language)
        sentences = []

        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret
