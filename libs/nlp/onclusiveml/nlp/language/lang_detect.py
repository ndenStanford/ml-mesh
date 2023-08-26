"""Language Detection."""

# Standard Library
from typing import Any, Callable, List, Optional

# 3rd party libraries
from langdetect import detect

# Internal libraries
from onclusiveml.nlp.language import constants
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.language.lang_exception import (
    LanguageDetectionException,
    LanguageFilterException,
)


def detect_language(content: str, language: Optional[str] = None) -> LanguageIso:
    """Detects language of given content

    Args:
        content (str): Content for which langugage needs to be detected
        language (Optional[str]): Optional parameter specifying the language. If provided,
            will convert to languageIso equivalent

    Returns:
        LanguageIso: Detected language represented as LanguageIso Enum value
    """
    if language:
        return constants.LanguageIso.from_language_iso(language)
    else:
        res = detect(content)
        return constants.LanguageIso.from_language_iso(res)


def filter_language(
    supported_languages: List[LanguageIso], raise_if_none: Optional[bool] = True
) -> Callable:
    """Decorator that filters supported language for a given function.

    Args:
        supported_languages (List[LanguageIso]): List of supported languages
    Returns:
        Callable: callable

    Example usage:
        @filter_language([LanguageIso.EN, LanguageIso.ES])
        def some_function(content: str, language: Optional[str] = None) -> Any:
            ...
        The decorated function "some_function" will only be executed if the detected
            language is supported
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(content: str, language: Optional[str] = None) -> Any:
            """Wrapper function that filters the supported languages before executing decorated function.

            Args:
                content (str): Content for which langugage needs to be detected
                language (Optional[str]): Optional parameter specifying the language. If provided,
                    will convert to languageIso equivalent

            Returns:
                Any: If detected language is supported, it will return the function and proceed.
                    Else will return None if the detected language is not in the list of supported
                    languages

            """
            lang = detect_language(content=content, language=language)
            if lang is None:
                if raise_if_none:
                    raise LanguageDetectionException(language=language)
                else:
                    return None
            else:
                if lang in supported_languages:
                    return func(content, lang)
                else:
                    raise LanguageFilterException(language=lang)

        return wrapper

    return decorator
