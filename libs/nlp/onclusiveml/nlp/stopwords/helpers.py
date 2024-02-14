"""Helpers."""

# Standard Library
import json
import os
from functools import lru_cache
from typing import List

# Internal libraries
# Internal Libraries
from onclusiveml.nlp.stopwords.exception import StopwordsFileException


def _get_stopword_filepath(lang: str) -> str:
    """Returns file path for the stopword file of a given language.

    Args:
        lang (str): The language for which the stopword file path is required

    Returns:
        str; File path for the stopword file

    """
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, "data", f"{lang}.json")


@lru_cache()
def load_stop_words_file(lang: str) -> List[str]:
    """Loads stopwords from the corresponding file for a given language.

    Args:
        lang (str): The language for which the stopwords are to be loaded

    Returns:
        List[str]: The list of stopwords for the specified language

    Raises:
        StopwordsFileException: If the stopword file for the specified language is not found
    """
    content: List[str] = []
    if lang == "all":
        directory = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(directory, "data")
        for stopwords_file in os.listdir(base_dir):
            with open(os.path.join(base_dir, stopwords_file)) as f:
                content = content + json.loads(f.read())
    else:
        try:
            with open(_get_stopword_filepath(lang)) as f:
                content = json.loads(f.read())
        except FileNotFoundError:
            raise StopwordsFileException(language=lang)
    return content
