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
        max_tokens: int,
        lang: str,
    ) -> str:
        """Summarization prediction handler method.
        Args:
            text (str):
            max_tokens (int):
            lang (str):
        """
        prompt_id = self.get_prompt(lang)
        input_dict = {"max_tokens": max_tokens, "content": text}
        #prompt = prompt.format(**input_dict)
        headers = {"x-api-key": settings.PROMPT_API_KEY}
        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(settings.PROMPT_API, prompt_id),
            headers=headers,
            json=input_dict
        )
        return eval(q.content)["generated"]

    def postprocess(self, text: str) -> str:
        text = re.sub("\n+", " ", text)
        return text

    def pre_process(self, text: str) -> str:
        text = re.sub("\n+", " ", text)
        return text

    def get_prompt(self, lang):
        headers = {"x-api-key": settings.PROMPT_API_KEY}
        q = requests.get(
            "{}/api/v1/prompts".format(settings.PROMPT_API), headers=headers
        )
        prompts = eval(q.content)["prompts"]
        english_prompt_dict = [
            prompt
            for prompt in prompts
            if prompt["alias"] == settings.PROMPT_DICT[lang]["alias"]
        ]
        prompt_id = english_prompt_dict[0]["id"]
        return prompt_id

        #q = requests.get(
        #    "{}/api/v1/prompts/{}".format(settings.PROMPT_API, prompt_id),
        #    headers=headers,
        #)
        #template = eval(q.content)["template"]
        #return template, prompt_id


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
        max_tokens = data["max_tokens"]
        top_p = data["top_p"]  # may be removed
        temperature = data["temperature"]
        presence_penalty = data["presence_penalty"]  # may be removed
        frequency_penalty = data["frequency_penalty"]  # may be removed
        model = data["model"]
        lang = data["lang"]

        starttime = datetime.datetime.utcnow()
        summary = _service.inference(
            text,
            max_tokens,
            lang,
        )
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        summary = _service.postprocess(summary)
        return {"model": model, "summary": summary}
    except Exception as e:
        raise e
