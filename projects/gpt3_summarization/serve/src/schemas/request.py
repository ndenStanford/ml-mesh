"""Request model."""

from typing import Optional

from pydantic import BaseModel


class Request(BaseModel):
    """GPT3 input request item."""

    content: Optional[str] = "" # NOTE: an empty string is needed (at least).
    max_tokens: Optional[int] = 512   # fix the max_tokens of the API, default for OpenAI's api is 16
    desired_length: Optional[int] = 100    # desired token length of summary, used in the prompt
    temperature: Optional[float] = 0.7   # temperature should be float between 0-2, default for OpenAI's API is 1
    top_p: Optional[float] = 1   # float ranged from 0-1, default 1, recommended not altering both temperatued and top_p
    presence_penalty: Optional[float] = 0    # float between -2.0 and 2.0, default 0
    frequency_penalty: Optional[float] = 0   # float between -2.0 and 2.0, default 0
    model: Optional[str] = "gpt-3.5-turbo"   # or "text-davinci-003"
