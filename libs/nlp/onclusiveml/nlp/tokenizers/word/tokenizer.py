"""Word tokenizer."""

# Standard Library
import re
from typing import Any, Dict, List

# 3rd party libraries
import jieba
import nltk
from konlpy.tag import Okt
from konoha import WordTokenizer


nltk.download("punkt")

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.word.base_tokenizer import BaseWordTokenizer


class NLTKWordTokenizer(BaseWordTokenizer):
    """Tokenizing words in a given text."""

    regex = re.compile(r"|".join(SPECIAL_CHARACTERS))

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
    """Tokenizing words in a given text."""

    def tokenize(self, content: str) -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized words
        """
        words = jieba.lcut(content)

        ret = {"words": words}

        return ret


class KonlpyWordTokenizer(BaseWordTokenizer):
    """Tokenizing words in a given text."""

    def tokenize(self, content: str) -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized words
        """
        tokenizer_okt = Okt()
        words = tokenizer_okt.morphs(content)

        ret = {"words": words}

        return ret


class MeCabWordTokenizer(BaseWordTokenizer):
    """Tokenizing words in a given text."""

    def tokenize(self, content: str) -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized words
        """
        tokenizer = WordTokenizer("MeCab")
        words = tokenizer.tokenize(content)

        ret = {"words": words}

        return ret
