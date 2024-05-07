"""Summarization handler."""

# Standard Library
import datetime
import re
from typing import Any, Dict, Optional

# 3rd party libraries
# OpenAI library
import openai
import requests

# Internal libraries
# Internal library
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import settings  # type: ignore[attr-defined]


# OpenAI api key
openai.api_key = settings.OPENAI_API_KEY

logger = get_default_logger(__name__)


class SummarizationHandler:
    """Summarization handler."""

    def inference(
        self,
        text: str,
        desired_length: int,
        lang: str,
        target_lang: str,
    ) -> str:
        """Summarization prediction handler method.

        Args:
            text (str): Text to summarize
            desired_length (int): desired length of the summary
            lang (str): input language of the summary
            target_lang (str): target language
        """
        try:
            alias = settings.PROMPT_DICT[lang][target_lang]["alias"]
        except KeyError:
            logger.errror("Summarization language not supported.")

        input_dict = {"input": {"desired_length": desired_length, "content": text}}
        headers = {"x-api-key": settings.INTERNAL_ML_ENDPOINT_API_KEY}

        q = requests.post(
            "{}/api/v2/prompts/{}/generate/model/{}".format(
                settings.PROMPT_API, alias, settings.SUMMARIZATION_DEFAULT_MODEL
            ),
            headers=headers,
            json=input_dict,
        )
        return eval(q.content)["generated"]

    def postprocess(self, text: str) -> str:
        """Post process text."""
        text = re.sub("\n+", " ", text)
        return text

    def pre_process(self, text: str) -> str:
        """Pre process text."""
        text = re.sub("\n+", " ", text)
        return text


_service = SummarizationHandler()


def handle(data: Any) -> Optional[Dict[str, str]]:
    """Handles prediction."""
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
                "Content field is empty. This will result in no summary being returned"
            )

        text = _service.pre_process(data["content"])
        desired_length = data["desired_length"]
        lang = data["lang"]
        target_lang = data["target_lang"]

        starttime = datetime.datetime.utcnow()
        summary = _service.inference(text, desired_length, lang, target_lang)
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        summary = _service.postprocess(summary)
        return {"summary": summary}
    except Exception as e:
        raise e
