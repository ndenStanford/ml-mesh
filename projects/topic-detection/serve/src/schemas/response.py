"""Response model."""

# Standard Library
from typing import Dict

# 3rd party libraries
from pydantic import BaseModel


class Response(BaseModel):
    """GPT topic analysis response item.

    Holds the information on expected output at inference

    Attributes:
        topic (dict): Aggregate the trends for each category in dict
    """

    topic: Dict
