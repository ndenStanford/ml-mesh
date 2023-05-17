"""Summarization handler."""

# Standard Library
import datetime
import re
from typing import Any, Dict, Optional, Tuple

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
        max_tokens: int,
        top_p: float,
        temperature: float,
        presence_penalty: float,
        frequency_penalty: float,
        model: str,
        lang: str,
    ) -> Tuple[str, str]:
        """Summarization prediction handler method.
        Args:
            text (str):
            desired_length (int):
            max_tokens (int):
            top_p (int):
            temperature (float):
            presence_penalty (float):
            frequency_penalty (float):
            model (str):
            lang (str):
        """
        prompt = self.get_prompt(lang)
        input_dict = {"max_tokens": max_tokens, "content": text}
        prompt = prompt.format(**input_dict)

        if model == "gpt-3.5-turbo":
            # get summary
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            summary = response["choices"][0]["message"]["content"]
        else:
            # get summary
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                max_tokens=max_tokens,  # default 16
                temperature=temperature,
            )

            summary = response["choices"][0]["text"]

        finish_reason = response["choices"][0]["finish_reason"]

        return summary, finish_reason

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
        english_prompt_id = english_prompt_dict[0]["id"]

        q = requests.get(
            "{}/api/v1/prompts/{}".format(settings.PROMPT_API, english_prompt_id),
            headers=headers,
        )
        template = eval(q.content)["template"]
        return template


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
        summary, finish_reason = _service.inference(
            text,
            desired_length,
            max_tokens,
            top_p,
            temperature,
            presence_penalty,
            frequency_penalty,
            model,
            lang,
        )
        endtime = datetime.datetime.utcnow()

        logger.debug(
            "Total Time in milliseconds = {}".format(
                (endtime - starttime).total_seconds() * 1000
            )
        )

        summary = _service.postprocess(summary)
        return {"model": model, "summary": summary, "finish_reason": finish_reason}
    except Exception as e:
        raise e
