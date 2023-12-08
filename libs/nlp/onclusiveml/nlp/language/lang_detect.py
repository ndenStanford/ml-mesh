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
    """Detects language of given content.

    Args:
        content (str): Content for which langugage needs to be detected
        language (Optional[str]): Optional parameter specifying the language. If provided,
            will convert to languageIso equivalent

    Returns:
        LanguageIso: Detected language represented as LanguageIso Enum value
    """
    if language is None:
        language = detect(content)

    return constants.LanguageIso.from_language_iso(language)


def filter_language(
    supported_languages: List[LanguageIso], raise_if_none: Optional[bool] = True
) -> Callable:
    """Decorator that filters supported language for a given function.

    Args:
        supported_languages (List[LanguageIso]): List of supported LanguageIso's
        raise_if_none (bool): raises error if language is not supported
    Returns:
        Callable: callable
    Raises:
        LanguageDetectionException: If not language could be detected, this error is raised.
        LanguageFilterException: If a language could be detected but is not a member of the
            supported_languages list, this error is raised.

    Example usage:
        @filter_language([LanguageIso.EN, LanguageIso.ES])
        def some_function(content: str, language: Optional[str] = None) -> Any:
            ...
        The decorated function "some_function"
            - needs to be called with `content` and `language` as keyword arguments
            - will only be executed if the detected language is supported
    """
    supported_language_iso_values = [
        supported_language.value for supported_language in supported_languages
    ]

    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Wrapper that filters the supported languages before executing decorated function.

            Returns:
                Any: If detected language is supported, it will return the function and proceed.
                    Else will return None if the detected language is not in the list of supported
                    languages

            """
            content, language = kwargs["content"], kwargs["language"]

            language_iso = detect_language(content=content, language=language)

            if language_iso is None:
                if raise_if_none:
                    raise LanguageDetectionException(
                        language_iso_value=language,
                        supported_language_iso_values=supported_language_iso_values,
                        supported_language_isos=supported_languages,
                    )
                else:
                    return None
            else:
                if language_iso in supported_languages:
                    kwargs["language"] = language_iso.value
                    return func(*args, **kwargs)
                else:
                    raise LanguageFilterException(
                        language_iso=language_iso,
                        supported_language_isos=supported_languages,
                    )

        return wrapper

    return decorator
