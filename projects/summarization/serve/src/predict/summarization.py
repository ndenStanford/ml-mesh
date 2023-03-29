"""Summarization handler."""

import re
import datetime

# Source
from src.settings import settings

# Internal library
from onclusiveml.core.logger import get_default_logger

# OpenAI library
import openai

# OpenAI api key
openai.api_key = settings.OPENAI_API_KEY

logger = get_default_logger(__name__)


class SummarizationHandler:
    def __init__(self):
        super().__init__()

    def inference(
        text,
        desired_length,
        max_tokens,
        top_p,
        temperature,
        presence_penalty,
        frequency_penalty,
        model,
    ):
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
        """

        # append summary prompt
        prompt = (
            "Give an abstractive summary while retaining important quotes of speech in less than "
            + str(desired_length)  # noqa: W503
            + " words: "  # noqa: W503
            + "\n"  # noqa: W503
            + text  # noqa: W503
            + "\n"  # noqa: W503
        )

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

    def postprocess(self, text):
        text = re.sub("\n+", " ", text)
        return text

    def pre_process(self, text):
        text = re.sub("\n+", " ", text)
        return text


_service = SummarizationHandler()


def handle(data):

    try:
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
