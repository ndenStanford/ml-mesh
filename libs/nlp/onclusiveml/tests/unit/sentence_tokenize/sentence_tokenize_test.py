"""Sentence tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp import SentenceTokenizer
from onclusiveml.nlp.sentence_tokenize.consts import SPECIAL_CHARACTERS


def test_tokenize():
    text = """Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.
    The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth."""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text)
    assert res["sentences"] == [
        "Elon Musk was the second person ever to amass a personal fortune of more than $200 billion, breaching that threshold in January 2021, months after Jeff Bezos.",  # noqa: E501
        "The Tesla Inc. chief executive officer has now achieved a first of his own: becoming the only person in history to erase $200 billion from their net worth.",  # noqa: E501
    ]


def test_tokenize_fr():
    text = """Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud.
    Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne.
    Après le divorce de ses parents en 1979, il continue de vivre avec son père. À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars"""  # noqa: E501
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=text, language="french")
    assert res["sentences"] == [
        "Elon Reeve Musk naît le 28 juin 1971 à Pretoria, en Afrique du Sud.",
        "Il est le fils d'Errol Musk, riche ingénieur et promoteur immobilier sud-africain aux origines afrikaner et anglo-sud-africaine, ayant eu des parts d’une mine d'émeraudes en Zambie, et de Maye Haldeman, une nutritionniste et mannequin canadienne.",  # noqa: E501
        "Après le divorce de ses parents en 1979, il continue de vivre avec son père.",
        "À l'âge de 12 ans, il vend son premier programme de jeu vidéo pour l'équivalent de 500 dollars",  # noqa: E501
    ]


@pytest.mark.parametrize(
    "char",
    SPECIAL_CHARACTERS,
)
def test_tokenize_unique_chars(char):
    sent1 = "This is sentence one"
    sent2 = "This is sentence two."
    test_sent = sent1 + char + sent2
    tokenizer = SentenceTokenizer()
    res = tokenizer.tokenize(content=test_sent)
    assert res["sentences"] == ["This is sentence one", "This is sentence two."]
