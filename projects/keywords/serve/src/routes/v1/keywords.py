"""Keybert predictions."""

# Standard Library
from typing import Dict, List, Optional, Union

# 3rd party libraries
from fastapi import APIRouter, status

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.keybert import handle
from src.schemas import Request, Response


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/keywords",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_keywords(item: Request) -> Optional[Dict[str, List[Union[str, float]]]]:
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
