"""Response model."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import BaseModel


class Response(BaseModel):
    """Summarization response item.

    Holds the information on expected output at inference

    Attributes:
        summary (str): Summary text in string
        finish_reason (str): String - Explain whether API returned full completion
            - stop means it has outputted complete summary
            - length means it has been cut short
        model (str): OpenAI model used to create summary
    """

    summary: str
