"""Response model."""

# Standard Library
from typing import List

# 3rd party libraries
from pydantic import BaseModel


class Response(BaseModel):
    keywords: List[str]
    probs: List[float]
