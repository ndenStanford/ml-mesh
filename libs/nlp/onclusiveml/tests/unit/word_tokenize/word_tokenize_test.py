"""Word tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.word import WordTokenizer


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
    res = tokenizer.tokenize(content=text, language="fr")
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


def test_word_tokenize_de():
    """Test word tokenizer German."""
    text = """Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "war",
        "der",
        "zweite",
        "Mensch",
        "überhaupt",
        ",",
        "der",
        "ein",
        "Privatvermögen",
        "von",
        "mehr",
        "als",
        "200",
        "Milliarden",
        "US-Dollar",
        "anhäufte",
        "und",
        "überschritt",
        "diese",
        "Schwelle",
        "im",
        "Januar",
        "2021",
        ",",
        "Monate",
        "nach",
        "Jeff",
        "Bezos",
        ".",
    ]  # noqa: E501


def test_word_tokenize_it():
    """Test word tokenizer Italian."""
    text = """Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "è",
        "stata",
        "la",
        "seconda",
        "persona",
        "in",
        "assoluto",
        "ad",
        "accumulare",
        "una",
        "fortuna",
        "personale",
        "di",
        "oltre",
        "200",
        "miliardi",
        "di",
        "dollari",
        ",",
        "superando",
        "quella",
        "soglia",
        "nel",
        "gennaio",
        "2021",
        ",",
        "mesi",
        "dopo",
        "Jeff",
        "Bezos",
        ".",
    ]  # noqa: E501


def test_word_tokenize_es():
    """Test word tokenizer Spanish."""
    text = """Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "fue",
        "la",
        "segunda",
        "persona",
        "en",
        "amasar",
        "una",
        "fortuna",
        "personal",
        "de",
        "más",
        "de",
        "200",
        "mil",
        "millones",
        "de",
        "dólares",
        ",",
        "superando",
        "ese",
        "umbral",
        "en",
        "enero",
        "de",
        "2021",
        ",",
        "meses",
        "después",
        "de",
        "Jeff",
        "Bezos",
        ".",
    ]


def test_word_tokenize_ca():
    """Test word tokenizer Catalan."""
    text = """Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos."""  # noqa: E501
    tokenizer = WordTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["words"] == [
        "Elon",
        "Musk",
        "va",
        "ser",
        "la",
        "segona",
        "persona",
        "que",
        "va",
        "acumular",
        "una",
        "fortuna",
        "personal",
        "de",
        "més",
        "de",
        "200.000",
        "milions",
        "de",
        "dòlars",
        ",",
        "superant",
        "aquest",
        "llindar",
        "el",
        "gener",
        "del",
        "2021",
        ",",
        "mesos",
        "després",
        "de",
        "Jeff",
        "Bezos",
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
