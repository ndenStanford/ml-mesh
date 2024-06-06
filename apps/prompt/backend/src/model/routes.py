"""Model."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status

# Internal libraries
from onclusiveml.llm.prompt_validator import PromptInjectionException

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
def generate(alias: str, prompt: str, validate_prompt: Optional[bool] = False):
    """Generates text using a prompt template."""
    try:
        return {"generated": F.generate_from_prompt(prompt, alias, validate_prompt)}
    except PromptInjectionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
