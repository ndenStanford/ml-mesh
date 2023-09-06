"""Request model."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel


class Request(BaseModel):
    """GPT topic analysis request item.

    Holds the required information to be provided in the payload and their type

    Attributes:
        content (List(str)): Text to generate summarization for. An empty string is needed

        max_tokens (int): Maximum number of tokens to generate in the completion.

        temperature (float): Should be float between 0-2, default for OpenAI's API
        is 1. Higher the value, the more random the output. Lower the value is more deterministic

        top_p (float): Nucleus sampling, where model considers results of the tokens with top_p
            probability mass. Float ranged from 0-1, default 1. Recommended not altering both
            temperature and top_p

        presence_penalty (float): Penalize new tokens based on whether they appear in text so far,
        increasing model's likelihood to talk about new topics. Between -2.0-2.0, default 0

        frequency_penalty (float): Positive values penalize new tokens based on existing
        frequency in text so far, decreasing model's likelihood to repeat same line verbatim.
        Float between -2.0 and 2.0, default 0

        model (str): model to use from OpenAI api
    """  # noqa: E501

    content: List[str] = [""]
    industry: str = ""
    max_tokens: Optional[int] = 8192
    temperature: Optional[float] = 1
    top_p: Optional[float] = 1
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    model: Optional[str] = "gpt-4"
