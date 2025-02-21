"""Stopwords test."""

# Standard Library
import json
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.stopwords import stopwords
from onclusiveml.nlp.stopwords.exception import StopwordsFileException
from onclusiveml.nlp.stopwords.helpers import load_stop_words_file


stopword_file = os.listdir("libs/nlp/onclusiveml/nlp/stopwords/data/")


@pytest.mark.parametrize(
    "stopword_file",
    stopword_file,
)
def test_get_load_stop_words(stopword_file):
    """Test get load stop words."""
    res = load_stop_words_file(lang=stopword_file[:-5])

    f = open("libs/nlp/onclusiveml/nlp/stopwords/data/" + stopword_file)
    stopwords = json.load(f)
    assert res == stopwords


def test_get_load_stop_words_exception():
    """Test get load stop words with exception."""
    with pytest.raises(StopwordsFileException, match="No stopword file found for xyz"):
        res = load_stop_words_file(lang="xyz")  # noqa: F841


@pytest.mark.parametrize(
    "content, language, lowercase, expected",
    [
        (
            ["Hello", "everyone", "my", "name", "is", "ML-Mesh"],
            "en",
            False,
            ["Hello", "ML-Mesh"],
        ),
        (
            ["Hello", "everyone", "my", "name", "is", "ML-Mesh"],
            "en",
            True,
            ["ml-mesh"],
        ),
        (
            [],
            "en",
            False,
            [],
        ),
        (
            None,
            "en",
            False,
            [],
        ),
    ],
)
def test_stopwords_function(content, language, lowercase, expected):
    """Test stopwords function."""
    res = stopwords(lang=language, content=content, lowercase=lowercase)
    assert res == expected
