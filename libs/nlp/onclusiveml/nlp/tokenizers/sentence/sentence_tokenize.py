"""Sentence Tokenize."""

# Standard Library
from typing import Any, Dict, List, Optional

# Internal libraries
from onclusiveml.nlp.language.constants import LanguageIso
from onclusiveml.nlp.tokenizers.consts import ALL_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.sentence.factory import sentence_factory


class SentenceTokenizer:
    """Tokenizing sentences in a given text."""

    factory = sentence_factory
    all_support_lang = ALL_SUPPORTED_LANGS

    def tokenize(
        self, content: str, language: Optional[str] = "en"
    ) -> Dict[str, List[Any]]:
        """Tokenizes the input content.

        Args:
            content (str): Text to be tokenized
            language (str, optional): Language of the text to be tokenized

        Returns:
            dict: Dictionary containing tokens
        """
        lang_iso = LanguageIso.from_language_iso(language)
        # Default to English if the specified language is not langIso
        if not lang_iso:
            lang_iso = LanguageIso.EN

        lang_simplified = next(iter(lang_iso.locales.values()))["en"].lower()
        if lang_simplified in self.all_support_lang:
            tokenizer = self.factory.get_tokenizer(lang_simplified)
        else:
            tokenizer = self.factory.get_tokenizer("english")

        ret = tokenizer.tokenize(content, lang_simplified)
        return ret
