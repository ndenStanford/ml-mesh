"""Model."""

# Standard Library
import json
from typing import List

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, Header, HTTPException, status

# Source
from src.model.tables import LanguageModel
from src.prompt import functional as F


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


@router.post("/{alias}/generate", status_code=status.HTTP_200_OK)
def generate(alias: str, prompt: str, model_parameters: str = Header(None)):
    """Generates text using a prompt template."""
    if model_parameters is not None:
        model_parameters = json.loads(model_parameters)
    return {
        "generated": F.generate_from_prompt(
            prompt, alias, model_parameters=model_parameters
        )
    }
