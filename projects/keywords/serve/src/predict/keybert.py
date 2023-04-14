"""Keybert handler."""

# Standard Library
import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

# ML libs
from keybert import KeyBERT

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings


logger = get_default_logger(__name__)


class KeybertHandler:

    _model = KeyBERT(model=settings.MODEL_NAME)

    def inference(
        self,
        text: str,
        keyphrase_ngram_range: Tuple,
        use_maxsum: bool,
        use_mmr: bool,
        diversity: float,
        nr_candidates: int,
        top_n: int,
    ) -> List:
        """Keybert prediction handler method.

        Args:
            keyphrase_ngram_range (Tuple):
            use_maxsum (bool):
            use_mmr (bool):
            diversity (float):
            nr_candidates (int):
            top_n (int):
        """
        return self.model.extract_keywords(
            text,
            keyphrase_ngram_range=keyphrase_ngram_range,
            use_maxsum=use_maxsum,
            use_mmr=use_mmr,
            diversity=diversity,
            nr_candidates=nr_candidates,
            top_n=top_n,
        )

    def postprocess(self, key_word: List[List]) -> Dict[str, List[Union[str, float]]]:
        """Postprocessing model prediction.

        Args:
            key_word (List): list of
        """
        words = [item[0] for item in key_word]
        prob = [item[1] for item in key_word]
        res = {"keywords": words, "probs": prob}
        return res

    @property
    def model(self) -> KeyBERT:
        return self._model


_service = KeybertHandler()


def handle(data: Any) -> Optional[Dict[str, List[Union[str, float]]]]:
    """Prediction handler."""
    try:

        if data is None:
            return None

        if "body" not in data[0]:
            logger.warning(
                "Malformed request, content does not contain a body key."
                "Is your request properly formatted as json?"
            )
            return None

        data = data[0]["body"]

        if type(data) == bytearray:
            data = eval(data)

        content = data["content"]
        if content is None or content == "":
            logger.warning(
                "Content field is empty. This will result in no key words being returned"
            )

        keyphrase_ngram_range = data["keyphrase_ngram_range"]
        use_maxsum = data["use_maxsum"]
        use_mmr = data["use_mmr"]
        diversity = data["diversity"]
        nr_candidates = data["nr_candidates"]
        top_n = data["top_n"]

        starttime = datetime.datetime.utcnow()

        keywords = _service.inference(
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

        return _service.postprocess(keywords)
    except Exception as e:
        raise e
