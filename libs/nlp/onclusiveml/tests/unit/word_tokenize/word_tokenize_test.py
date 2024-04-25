"""Word tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.tokenize.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenize.word import WordTokenizer


def test_word_tokenize():
    """Test word tokenizer."""
    text = """
    Elon Musk was the second person ever to amass a personal fortune of more than $200 billion,
    breaching that threshold in January 2021, months after Jeff Bezos.
    """
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text)
    assert res["words"] == [
        "Elon",
        "Musk",
        "was",
        "the",
        "second",
        "person",
        "ever",
        "to",
        "amass",
        "a",
        "personal",
        "fortune",
        "of",
        "more",
        "than",
        "$",
        "200",
        "billion",
        ",",
        "breaching",
        "that",
        "threshold",
        "in",
        "January",
        "2021",
        ",",
        "months",
        "after",
        "Jeff",
        "Bezos",
        ".",
    ]


def test_word_tokenize_fr():
    """Test word tokenizer French."""
    text = """Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="french")
    assert res["words"] == [
        "Elon",
        "Reeve",
        "Musk",
        "naît",
        "le",
        "28",
        "juin",
        "1971",
        "à",
        "Pretoria",
        ",",
        "en",
        "Afrique",
        "du",
        "Sud",
        ".",
    ]  # noqa: E501


@pytest.mark.parametrize(
    "char",
    SPECIAL_CHARACTERS,
)
def test_word_tokenize_unique_chars(char):
    """Test word tokenizer on unique characters."""
    word1 = "one"
    word2 = "two"
    test_word = word1 + char + word2
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=test_word)
    assert res["words"] == [word1, word2]
