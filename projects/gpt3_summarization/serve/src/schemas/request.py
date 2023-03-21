"""Request model."""

from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    """GPT3 request item.

    Holds the required information to be provided in the payload and their type

    Attributes:
        content (str): Text to generate summarization for. An empty string is needed (at least)

        max_tokens (int): Maximum number of tokens to generate in the completion. Default for
        OpenAI's api is 16

        desired_length (int): Desired token length of summary used in the prompt

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
    """

    content: Optional[str] = ""
    max_tokens: Optional[int] = 512
    desired_length: Optional[int] = 100
    temperature: Optional[float] = 0.7

    top_p: Optional[float] = 1
    presence_penalty: Optional[float] = 0
    frequency_penalty: Optional[float] = 0
    model: Optional[str] = "gpt-3.5-turbo"
