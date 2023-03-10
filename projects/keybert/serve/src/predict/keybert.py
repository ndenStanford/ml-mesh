"""Keybert handler."""

import datetime

from src.settings import settings
from onclusiveml.core.logger import get_default_logger

from keybert import KeyBERT


logger = get_default_logger(__name__)


class KeybertHandler:
    def __init__(self):
        super().__init__()
        self.initialized = False

    def inference(
        self,
        text,
        keyphrase_ngram_range,
        use_maxsum,
        use_mmr,
        diversity,
        nr_candidates,
        top_n,
    ):
        key_word = self.model.extract_keywords(
            text,
            keyphrase_ngram_range=keyphrase_ngram_range,
            use_maxsum=use_maxsum,
            use_mmr=use_mmr,
            diversity=diversity,
            nr_candidates=nr_candidates,
            top_n=top_n,
        )
        return key_word

    def postprocess(self, key_word):
        words = [item[0] for item in key_word]
        prob = [item[1] for item in key_word]
        res = {"keywords": words, "probs": prob}
        return res

    def initialize(self):
        self.model = KeyBERT(model=settings.MODEL_NAME)
        self.initialized = True


_service = KeybertHandler()


def handle(data):

    try:
        if not _service.initialized:
            _service.initialize()

        if data is None:
            return None

        if "body" not in data[0]:
            logger.error(
                "Malformed request, content does not contain a body key."
                "Is your request properly formatted as json?"
            )
            return None

        data = data[0]["body"]

        if type(data) == bytearray:
            data = eval(data)

        content = data["content"]
        if content is None or content == "":
            logger.error(
                "Content field is empty. This will result in no key words being returned"
            )

        keyphrase_ngram_range = data["keyphrase_ngram_range"]
        use_maxsum = data["use_maxsum"]
        use_mmr = data["use_mmr"]
        diversity = data["diversity"]
        nr_candidates = data["nr_candidates"]
        top_n = data["top_n"]
        starttime = datetime.datetime.utcnow()
        key_words = _service.inference(
            content,
            keyphrase_ngram_range,
            use_maxsum,
            use_mmr,
            diversity,
            nr_candidates,
            top_n,
        )
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        key_words = _service.postprocess(key_words)
        return key_words
    except Exception as e:
        raise e
