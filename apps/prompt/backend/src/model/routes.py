"""Model."""

# Standard Library
from typing import List

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status

# Source
from src.model.exceptions import ModelNotFound
from src.model.tables import LanguageModel


router = APIRouter(
    prefix="/v2/models",
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=List[LanguageModel],
)
def list_models():
    """List models."""
    return LanguageModel.scan()


@router.get(
    "/{alias}",
    status_code=status.HTTP_200_OK,
    response_model=LanguageModel,
)
def get_model(alias: str):
    """Retrieves model via model alias.

    Args:
        alias (str): model alias
    """
    try:
        return LanguageModel.get(alias)
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
