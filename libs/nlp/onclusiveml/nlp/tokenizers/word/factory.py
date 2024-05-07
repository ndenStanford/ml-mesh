"""Word Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.factory import TokenizerFactory
from onclusiveml.nlp.tokenizers.word.tokenizer import (
    JiebaWordTokenizer,
    KonlpyWordTokenizer,
    MeCabWordTokenizer,
    NLTKWordTokenizer,
)


word_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    word_factory.register_language(lang, NLTKWordTokenizer())
word_factory.register_language("korean", KonlpyWordTokenizer())
word_factory.register_language("japanese", MeCabWordTokenizer())
word_factory.register_language("chinese", JiebaWordTokenizer())
# sudo yum install gcc-c++ java-1.8.0-openjdk-devel python3-devel python3-pip curl
