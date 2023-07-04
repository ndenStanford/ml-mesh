# Standard Library
import json
import os
from functools import lru_cache
from typing import List, Optional

# Internal libraries
# Internal Libraries
from onclusiveml.nlp.stopwords.stopwords_exception import StopwordsFileException


def _get_stopword_filepath(lang: str) -> str:
    """Returns stopword filename for a language."""
    directory = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directory, "data", f"{lang}.json")


@lru_cache()
def load_stop_words_file(lang: str) -> List[str]:
    """Loads stop words from file."""
    content = []
    try:
        with open(_get_stopword_filepath(lang)) as f:
            content = json.loads(f.read())
    except FileNotFoundError:
        raise StopwordsFileException(language=lang)
    return content
    # return files


def stopwords(
    lang: str, content: Optional[List[str]] = None, lowercase: Optional[bool] = False
) -> List[str]:
    if content:
        if len(content) > 0:
            if lowercase:
                content = list(map(str.lower, content))
            stopwords = load_stop_words_file(lang=lang)
            res = [words for words in content if words not in stopwords]
            return res
    return []
