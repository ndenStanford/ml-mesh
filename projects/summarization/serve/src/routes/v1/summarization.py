"""Summarization prediction."""

# Standard lib

# Standard Library
from typing import Dict, Optional

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.summarization import handle
from src.schemas import Request, Response


logger = get_default_logger(__name__)

router = APIRouter(prefix="/summarization/gpt3",)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_summary(item: Request,) -> Optional[Dict[str, str]]:
    """Returns summary of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: summary, model used and reason response finished.
    """
    summary = handle(
        data=[
            {
                "body": {
                    "content": item.content,
                    "desired_length": item.desired_length,
                    "max_tokens": item.max_tokens,
                    "top_p": item.top_p,
                    "temperature": item.temperature,
                    "presence_penalty": item.presence_penalty,
                    "frequency_penalty": item.frequency_penalty,
                    "model": item.model,
                }
            }
        ]
    )
    return summary
