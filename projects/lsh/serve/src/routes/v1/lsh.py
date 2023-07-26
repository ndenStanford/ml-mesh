"""Summarization prediction."""

# Standard lib

# Standard Library
from typing import Dict, List, Optional

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.lsh import handle
from src.schemas import Request, Response


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/lsh",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_lsh(
    item: Request,
) -> Optional[Dict[str, List[str]]]:
    """Returns signature of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: LSH signature.
    """
    #  language = item.language
    #  if language in ["zh-tw", "zh-cn"]:
    #      language = "zh"
    signature = handle(
        data=[
            {
                "body": {
                    "content": item.content,
                    "language": item.language,
                    "shingle_list": item.shingle_list,
                    "threshold": item.threshold,
                    "num_perm": item.num_perm,
                    "weights": item.weights,
                }
            }
        ]
    )
    return signature
