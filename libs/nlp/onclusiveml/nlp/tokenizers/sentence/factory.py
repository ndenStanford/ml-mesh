"""Sentence Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import (
    JA_LANG_SIMPLIFIED,
    KO_LANG_SIMPLIFIED,
    NLTK_SUPPORTED_LANGS,
    ZH_LANG_SIMPLIFIED,
)
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

sentence_factory.register_language(ZH_LANG_SIMPLIFIED, ZhSentenceTokenizer())
sentence_factory.register_language(KO_LANG_SIMPLIFIED, SpacySentenceTokenizer())
sentence_factory.register_language(JA_LANG_SIMPLIFIED, KonohaSentenceTokenizer())
