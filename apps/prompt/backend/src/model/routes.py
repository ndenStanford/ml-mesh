"""Model."""

# Standard Library
import json
import uuid
from typing import List

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, Header, HTTPException, status

# Source
from src.generated.tables import Generated
from src.model.tables import LanguageModel
from src.prompt import functional as F
from src.prompt.constants import CeleryStatusTypes


router = APIRouter(
    prefix="/v3/models",
)

# Standard Library
from datetime import datetime


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


@router.post("/{alias}/generate/async", status_code=status.HTTP_200_OK)
def generate_async(alias: str, prompt: str, model_parameters: str = Header(None)):
    """Generates text using a prompt template."""
    if model_parameters is not None:
        model_parameters = json.loads(model_parameters)
    else:
        model_parameters = {}

    custom_task_id = f"{uuid.uuid4().hex}"
    # Convert model parameters to strings for storage
    model_parameters = {k: str(v) for k, v in model_parameters.items()}

    generated = Generated(
        id=custom_task_id,
        status=CeleryStatusTypes.PENDING,
        generation=None,
        error=None,
        timestamp=datetime.now(),
        model=alias,
        prompt=prompt,
        model_parameters=model_parameters,
    )

    generated.save()
    # Submit the task with the custom ID
    F.generate_from_prompt.apply_async(
        args=[prompt, alias],
        kwargs={"model_parameters": model_parameters, "generated_id": custom_task_id},
        task_id=custom_task_id,
    )
    return generated
