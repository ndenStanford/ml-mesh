"""GPT3 Summarization prediction."""

from onclusiveml.core.logger import get_default_logger
from src.predict.gpt3_summarize import handle
from src.schemas import Request, Response

from fastapi import APIRouter, status


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/summarize/gpt3",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_summary(item: Request) -> Response:  # item is an instance of Item class
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
                    "text": item.content,
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
