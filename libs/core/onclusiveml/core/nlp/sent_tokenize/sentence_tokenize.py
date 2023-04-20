"Sentence Tokenize"

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import nltk


nltk.download("punkt")

# Internal libraries
# import consts
from onclusiveml.core.nlp.sent_tokenize.consts import TOKENS


class SentenceTokenize:

    regex = re.compile(r"|".join(TOKENS))

    def tokenize(self, content: str, language: str = "english") -> Dict[str, List[Any]]:

        sentences_first = nltk.sent_tokenize(content, language)
        sentences = []

        for sentence in sentences_first:
            s = self.regex.split(sentence)
            sentences += s

        ret = {"sentences": sentences}

        return ret
