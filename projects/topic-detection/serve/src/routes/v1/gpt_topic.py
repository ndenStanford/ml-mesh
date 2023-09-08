"""Topic detection prediction."""

# Standard lib

# Standard Library
from typing import Dict

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.gpt_topic import handle
from src.schemas import Request, Response
from src.settings import Settings


settings = Settings()

logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/topic/gpt4",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_gpt_analysis(
    item: Request,
) -> Dict[str, Dict]:
    """Return the topic deep analysis of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: category & analysis, model used and reason response finished.
    """
    topic = handle(
        data=[
            {
                "body": {
                    "content": item.content,
                    "industry": item.industry,
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
    return topic
