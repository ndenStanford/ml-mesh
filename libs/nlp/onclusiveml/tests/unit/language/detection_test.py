"""Sentence tokenizer test."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.nlp.language import detect_language, filter_language
from onclusiveml.nlp.language.constants import LanguageIso


def test_detect_language():
    text = "I am an engineer from London"
    lang = "en"
    res = detect_language(content=text, language=lang)
    assert res == LanguageIso.EN


def test_detect_language_unknown():
    text = "I am an engineer from London"
    lang = "UNKNOWN"
    res = detect_language(content=text, language=lang)
    assert res is None


def test_detect_language_content():
    text = "I am an engineer from London"
    res = detect_language(content=text)
    assert res == LanguageIso.EN


def test_detect_language_content_fr():
    text = "Je suis un ingénieur de Londres"
    res = detect_language(content=text)
    assert res == LanguageIso.FR


@pytest.mark.parametrize(
    "content, language, supported_languages, expected",
    [
        (
            "Hello world!",
            "en",
            [LanguageIso.EN],
            "Processing content: Hello world!",
        ),
        (
            "Salut comment tu t'appelles?",
            "fr",
            [LanguageIso.EN],
            "We currently do not support this language",
        ),
        (
            "Salut comment tu t'appelles?",
            "fr",
            [LanguageIso.EN, LanguageIso.FR],
            "Processing content: Salut comment tu t'appelles?",
        ),
        (
            "Hola, cómo estás",
            None,
            [LanguageIso.EN],
            "We currently do not support this language",
        ),
    ],
)
def test_detect_language_decorator(content, language, supported_languages, expected):
    @filter_language(supported_languages)
    def some_func(content: str, language: str = None) -> str:
        return "Processing content: " + content

    result = some_func(content, language)
    assert result == expected
