"""Response model."""

# 3rd party libraries
from pydantic import BaseModel


class Response(BaseModel):
    """Summarization response item.

    Holds the information on expected output at inference

    Attributes:
        summary (str): Summary text in string
    """

    summary: str
