"""Language Detection."""

# Standard Library
from typing import Any, Callable, Optional

# 3rd party libraries
from langdetect import detect

# Internal libraries
from onclusiveml.nlp.language import constants
from onclusiveml.nlp.language.constants import LanguageIso


def detect_language(content: str, language: Optional[str] = None) -> LanguageIso:
    if language:
        return constants.LanguageIso.from_language_iso(language)
    else:
        res = detect(content)
        return constants.LanguageIso.from_language_iso(res)


def filter_language(func: Callable) -> Any:
    def wrapper(content: str, language: Optional[str] = None) -> LanguageIso:
        lang = detect_language(content=content, language=language)
        if lang == LanguageIso.EN:
            return func(content, language)
        else:
            return "We currently do not support this language"

    return wrapper
