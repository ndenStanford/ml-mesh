"""Sentence Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.factory import TokenizerFactory
from onclusiveml.nlp.tokenizers.sentence.tokenizer import (
    KonohaSentenceTokenizer,
    NLTKSentenceTokenizer,
    SpacySentenceTokenizer,
    ZhSentenceTokenizer,
)


sentence_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    sentence_factory.register_language(lang, NLTKSentenceTokenizer())

sentence_factory.register_language("chinese", ZhSentenceTokenizer())
sentence_factory.register_language("korean", SpacySentenceTokenizer())
sentence_factory.register_language("japanese", KonohaSentenceTokenizer())
