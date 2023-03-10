"""Keybert predictions."""

from onclusiveml.core.logger import get_default_logger
from src.predict.keybert import handle
from src.schemas import Request, Response

from fastapi import APIRouter, status


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/keybert",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_keywords(item: Request) -> Response:  # item is an instance of Item class
    """Returns keywords sorted by relevance.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: list of keywords and relevance score.
    """
    keywords = handle(
        data=[
            {
                "body": {
                    "content": item.content,
                    "keyphrase_ngram_range": item.keyphrase_ngram_range,
                    "use_maxsum": item.use_maxsum,
                    "use_mmr": item.use_mmr,
                    "diversity": item.diversity,
                    "nr_candidates": item.nr_candidates,
                    "top_n": item.top_n,
                }
            }
        ]
    )
    return keywords
