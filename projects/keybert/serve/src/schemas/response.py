"""Response model."""

from typing import List

from pydantic import BaseModel


class Response(BaseModel):
    keywords: List[str]
    probs: List[float]
