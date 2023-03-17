"""Response model."""

from typing import List

from pydantic import BaseModel


class Response(BaseModel):
    model: str # model used for inference
    summary: str # summary response
    finish_reason: str # cause of finish
