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
from src.prompt.routes import get_task_status
from src.settings import Prediction
from src.prompt.constants import CeleryStatusTypes

router = APIRouter(
    prefix="/v3/models",
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

    task = F.generate_from_prompt.delay(
        prompt, alias, model_parameters=model_parameters
    )
    return Prediction(task_id=task.id, status=CeleryStatusTypes.PENDING, generated=None, error=None)


@router.get("/status/{task_id}", status_code=status.HTTP_200_OK)
def get_task_status_model(task_id: str):
    """Fetch the status or result of a Celery task."""
    return get_task_status(task_id)
