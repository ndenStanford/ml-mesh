"""Word Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import (
    JA_LANG_SIMPLIFIED,
    KO_LANG_SIMPLIFIED,
    NLTK_SUPPORTED_LANGS,
    ZH_LANG_SIMPLIFIED,
)
from onclusiveml.nlp.tokenizers.factory import TokenizerFactory
from onclusiveml.nlp.tokenizers.word.tokenizer import (
    JanomeWordTokenizer,
    JiebaWordTokenizer,
    NLTKWordTokenizer,
    SpacyWordTokenizer,
)


word_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    word_factory.register_language(lang, NLTKWordTokenizer())
word_factory.register_language(KO_LANG_SIMPLIFIED, SpacyWordTokenizer())
word_factory.register_language(JA_LANG_SIMPLIFIED, JanomeWordTokenizer())
word_factory.register_language(ZH_LANG_SIMPLIFIED, JiebaWordTokenizer())
