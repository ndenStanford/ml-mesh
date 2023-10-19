"""Helpers."""

# Standard Library
from typing import List, Optional

# Internal libraries
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file


def stopwords(
    lang: Optional[str] = None,
    content: Optional[List[str]] = None,
    lowercase: Optional[bool] = False,
) -> List[str]:
    """Filters out stop words from the provided content for a given language.

    Args:
        lang (str): The language for which stopwords are to be filtered
        content (Optional[List[str]]): Content from which stopwords are to be filtered.
            Defaults to None
        lowercase (Optional[bool]): Flag indicating whetehr to convert the content to lowercase
            before filtering out the stopwords. Defaults to false.
    """
    if content and lang:
        if len(content) > 0:
            if lowercase:
                content = list(map(str.lower, content))
            stopwords = load_stop_words_file(lang=lang)
            res = [words for words in content if words not in stopwords]
            return res
    return []
