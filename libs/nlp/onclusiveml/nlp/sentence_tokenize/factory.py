from onclusiveml.nlp.sentence_tokenize.base import BaseSentenceTokenizer
from onclusiveml.nlp.sentence_tokenize.nltk import NLTKSentenceTokenizer
from onclusiveml.nlp.sentence_tokenize.consts import NLTK_SUPPORTED_LANGS


class SentenceTokenizerFactory:

    def __init__(self):
        self._creators = {}

    def register_language(self, language: str, sentence_tokenizer: BaseSentenceTokenizer):
        self._creators[language] = sentence_tokenizer

    def get_sentence_tokenizer(self, language: str):
        creator = self._creators.get(language)
        if not creator:
            raise ValueError(language)
        return creator()


factory = SentenceTokenizerFactory()
for lang in NLTK_SUPPORTED_LANGS:
  factory.register_language(lang, NLTKSentenceTokenizer())