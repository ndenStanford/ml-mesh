"""Sentence Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenize.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.tokenize.factory import TokenizerFactory
from onclusiveml.nlp.tokenize.sentence.nltk_tokenizer import (
    NLTKSentenceTokenizer,
)


sentence_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    sentence_factory.register_language(lang, NLTKSentenceTokenizer())
