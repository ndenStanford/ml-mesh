"""Summarization prediction."""

# Standard lib

# Standard Library
from typing import Dict, Optional

# 3rd party libraries
# Third party libs
from fastapi import APIRouter, status, HTTPException

# Internal libraries
# Internal libs
from onclusiveml.core.logging import get_default_logger

# Source
from src.predict.summarization import handle
from src.schemas import Request, Response
from src.settings import settings


logger = get_default_logger(__name__)

router = APIRouter(
    prefix="/summarization/gpt3",
)


@router.post("/predict", response_model=Response, status_code=status.HTTP_200_OK)
def get_summary(
    item: Request,
) -> Optional[Dict[str, str]]:
    """Returns summary of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: summary, model used and reason response finished.
    """
    
    if item.lang not in settings.PROMPT_DICT.keys():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Language not supported",
        )
    
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
                    "lang": item.lang,
                    "target_lang": item.lang,
                }
            }
        ]
    )
    return summary

@router.post("/predict/{target_lang}", response_model=Response, status_code=status.HTTP_200_OK)
def get_summary(
    target_lang: str,
    item: Request,
) -> Optional[Dict[str, str]]:
    """Returns summary of item content.

    Args:
        item (Request): parse request arguments.

    Returns:
        Response: summary, model used and reason response finished.
    """

    target_lang_dict = settings.PROMPT_DICT.get(item.lang)
    if target_lang_dict is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Language not supported",
        )
    else:
        target_dict = target_lang_dict.get(target_lang)
        if target_dict is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Language not supported",
            )

        
    
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
                    "lang": item.lang,
                    "target_lang": target_lang,
                }
            }
        ]
    )
    return summary