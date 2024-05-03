"""Sentence tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import SPECIAL_CHARACTERS
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer


def test_tokenize():
    """Test SentenceTokenizer class for tokenizing english text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
    The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text)
    assert res["sentences"] == [
        "Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.",  # noqa: E501
        "The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.",  # noqa: E501
    ]


def test_tokenize_fr():
    """Test SentenceTokenizer class for tokenizing French text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud.
    Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne.
    Après le divorce de ses parents en 1979, il continue de vivre avec son père. À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars"""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="fr")
    assert res["sentences"] == [
        "Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud.",
        "Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne.",  # noqa: E501
        "Après le divorce de ses parents en 1979, il continue de vivre avec son père.",
        "À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars",  # noqa: E501
    ]


def test_tokenize_de():
    """Test SentenceTokenizer class for tokenizing German text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos.
    Dem Vorstandsvorsitzenden von Tesla Inc. ist nun ein Novum gelungen: Er ist der einzige Mensch in der Geschichte, der 200 Milliarden US-Dollar aus seinem Nettovermögen gestrichen hat."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="de")
    assert res["sentences"] == [
        "Elon Musk war der zweite Mensch überhaupt, der ein Privatvermögen von mehr als 200 Milliarden US-Dollar anhäufte und überschritt diese Schwelle im Januar 2021, Monate nach Jeff Bezos.",  # noqa: E501
        "Dem Vorstandsvorsitzenden von Tesla Inc.",
        "ist nun ein Novum gelungen: Er ist der einzige Mensch in der Geschichte, der 200 Milliarden US-Dollar aus seinem Nettovermögen gestrichen hat.",  # noqa: E501
    ]


def test_tokenize_it():
    """Test SentenceTokenizer class for tokenizing Italian text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos.
    L’amministratore delegato di Tesla Inc. ha ora raggiunto un primato: diventare l’unica persona nella storia a cancellare 200 miliardi di dollari dal proprio patrimonio netto."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="it")
    assert res["sentences"] == [
        "Elon Musk è stata la seconda persona in assoluto ad accumulare una fortuna personale di oltre 200 miliardi di dollari, superando quella soglia nel gennaio 2021, mesi dopo Jeff Bezos.",  # noqa: E501
        "L’amministratore delegato di Tesla Inc.",
        "ha ora raggiunto un primato: diventare l’unica persona nella storia a cancellare 200 miliardi di dollari dal proprio patrimonio netto.",  # noqa: E501
    ]


def test_tokenize_es():
    """Test SentenceTokenizer class for tokenizing Spanish text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos.
    El director ejecutivo de Tesla Inc. ha logrado ahora una primicia: convertirse en la única persona en la historia en borrar 200.000 millones de dólares de su patrimonio neto."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="es")
    assert res["sentences"] == [
        "Elon Musk fue la segunda persona en amasar una fortuna personal de más de 200 mil millones de dólares, superando ese umbral en enero de 2021, meses después de Jeff Bezos.",  # noqa: E501
        "El director ejecutivo de Tesla Inc.",
        "ha logrado ahora una primicia: convertirse en la única persona en la historia en borrar 200.000 millones de dólares de su patrimonio neto.",  # noqa: E501
    ]


def test_tokenize_ca():
    """Test SentenceTokenizer class for tokenizing Catalan text into a list of sentences.

    Returns:
        None
    """
    text = """Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos.
    El conseller delegat de Tesla Inc. ha aconseguit ara el seu primer: convertir-se en l'única persona de la història que ha esborrat 200.000 milions de dòlars del seu patrimoni net."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ca")
    assert res["sentences"] == [
        "Elon Musk va ser la segona persona que va acumular una fortuna personal de més de 200.000 milions de dòlars, superant aquest llindar el gener del 2021, mesos després de Jeff Bezos.",  # noqa: E501
        "El conseller delegat de Tesla Inc. ha aconseguit ara el seu primer: convertir-se en l'única persona de la història que ha esborrat 200.000 milions de dòlars del seu patrimoni net.",  # noqa: E501
    ]


def test_tokenize_unknown_language():
    """Test SentenceTokenizer with an unknown language should default to English tokenization."""
    text = """This is a sample English text. It contains multiple sentences."""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="xyz")
    assert res["sentences"] == [
        "This is a sample English text.",
        "It contains multiple sentences.",
    ]


def test_tokenize_unsupported_nltk_language():
    """Test SentenceTokenizer with a language that NLTK doesn't support."""
    text = """이것은 샘플 영어 텍스트입니다. 여러 문장이 포함되어 있습니다."""
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="ko")
    assert res["sentences"] == ["이것은 샘플 영어 텍스트입니다.", "여러 문장이 포함되어 있습니다."]


@pytest.mark.parametrize(
    "char",
    SPECIAL_CHARACTERS,
)
def test_tokenize_unique_chars(char):
    """Test SentenceTokenizer class for tokenizing text with unique characters.

    Args:
        char (str): A special character.

    Returns:
        None
    """
    sent1 = "This is sentence one"
    sent2 = "This is sentence two."
    test_sent = sent1 + char + sent2
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=test_sent)
    assert res["sentences"] == [sent1, sent2]
