"""Word tokenizer."""

# Standard Library
from typing import Any, Dict, List, Optional

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.tokenizers.consts import ALL_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.word.factory import word_factory


class WordTokenizer:
    """Tokenizing words in a given text."""

    factory = word_factory
    all_support_lang = ALL_SUPPORTED_LANGS

    def tokenize(
        self, content: str, language: Optional[str] = "en"
    ) -> Dict[str, List[Any]]:
        """Tokenizes the input content into words.

        Uses both nltk word tokenize and regex using list of unique characters

        Args:
            content (str): Text to be tokenized into words
            language (str, optional): Language of the text (default English)

        Returns:
            dict: Dictionary containing tokenized words
        """
        # return language iso equivalent of language e.g. fr is LanguageIso.FR
        langIso = LanguageIso.from_language_iso(language)
        # if LanguageIso of the language is not None, return english name of LanguageIso
        # e.g. LanguageIso.FR is french
        if langIso:
            lang_simplified = next(iter(langIso.locales.values()))["en"].lower()
        else:
            english_text = next(iter(LanguageIso.EN.locales.values()))["en"].lower()
            lang_simplified = english_text

        if lang_simplified in self.all_support_lang:
            tokenizer = self.factory.get_tokenizer(lang_simplified)
        else:
            lang_simplified = next(iter(LanguageIso.EN.locales.values()))["en"].lower()
            tokenizer = self.factory.get_tokenizer(lang_simplified)

        ret = tokenizer.tokenize(content, lang_simplified)
        return ret
