"""Word Tokenize Factory."""

# Internal libraries
from onclusiveml.nlp.tokenizers.consts import NLTK_SUPPORTED_LANGS
from onclusiveml.nlp.tokenizers.factory import TokenizerFactory
from onclusiveml.nlp.tokenizers.word.tokenizer import NLTKWordTokenizer


word_factory = TokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
    word_factory.register_language(lang, NLTKWordTokenizer())
