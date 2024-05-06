"""Word Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.factory import TokenizerFactory
from onclusiveml.nlp.tokenizers.word.nltk_tokenizer import (
    JiebaWordTokenizer,
    KonlpyWordTokenizer,
    MecabWordTokenizer,
    NLTKWordTokenizer,
)


word_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    word_factory.register_language(lang, NLTKWordTokenizer())
word_factory.register_language("ko", KonlpyWordTokenizer())
word_factory.register_language("ja", MecabWordTokenizer())
word_factory.register_language("zh", JiebaWordTokenizer())
