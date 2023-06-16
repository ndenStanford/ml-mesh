"""Helpers."""

# Standard Library
import json
import os
from functools import lru_cache
from typing import List


# NOTE: caching this function to avoid reading to the disk too often.


def _get_stopword_filepath(lang: str) -> str:
    """Returns stopword filename for a language."""
    return os.path.join("data", f"{lang}.json")


@lru_cache()
def load_stop_words_file(lang: str) -> List[str]:
    """Loads stop words from file."""
    with open(_get_stopword_filepath(lang)) as f:
        contents = json.loads(f.read())
    return contents
