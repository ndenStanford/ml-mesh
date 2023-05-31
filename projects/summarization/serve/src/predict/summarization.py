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
from src.settings import settings


# OpenAI api key
openai.api_key = settings.OPENAI_API_KEY

logger = get_default_logger(__name__)


class SummarizationHandler:
    def inference(
        self,
        text: str,
        desired_length: int,
        lang: str,
        target_lang: str,
    ) -> str:
        """Summarization prediction handler method.
        Args:
            text (str):
            desired_length (int):
            lang (str):
        """
        # prompt_id = self.get_prompt(lang)
        alias = settings.PROMPT_DICT[lang][target_lang]["alias"]
        input_dict = {"desired_length": desired_length, "content": text}
        # prompt = prompt.format(**input_dict)
        headers = {"x-api-key": settings.PROMPT_API_KEY}

        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, alias),
            headers=headers,
            json=input_dict,
        )
        return eval(q.content)["generated"]

    def postprocess(self, text: str) -> str:
        text = re.sub("\n+", " ", text)
        return text

    def pre_process(self, text: str) -> str:
        text = re.sub("\n+", " ", text)
        return text


_service = SummarizationHandler()


def handle(data: Any) -> Optional[Dict[str, str]]:

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
        summary = _service.inference(
            text,
            desired_length,
            lang,
            target_lang
        )
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
