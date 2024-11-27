"""Project."""

# Standard Library
import json
import uuid
from datetime import datetime
from json import JSONDecodeError
from typing import Any, Dict

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, Header, HTTPException, status
from langchain_core.exceptions import OutputParserException

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.generated.tables import Generated
from src.model.constants import MODELS_TO_PARAMETERS, ChatModel
from src.project.tables import Project
from src.prompt import functional as F
from src.prompt.constants import CeleryStatusTypes
from src.prompt.exceptions import PromptFieldsMissing, StrOutputParserTypeError
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()

router = APIRouter(
    prefix="/v3/prompts",
)
logger = get_default_logger(__name__)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_prompt(prompt: PromptTemplate):
    """Creates prompt in project.

    Args:
        prompt (PromptTemplate): prompt template object.
    """
    # if project does exist, create a new version
    try:
        _ = Project.get(prompt.project)
        prompt.save()
        return prompt
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {prompt.project} not found in database",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.put("/{alias}", status_code=status.HTTP_201_CREATED)
def update_prompt(template: Dict[str, str], alias: str):
    """Updates prompt in project.

    Args:
        template (str): updated prompt template.
        alias (str): prompt alias.
    """
    try:
        prompt = PromptTemplate.get(alias)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt {alias} not found in database",
        )
    try:
        prompt.template = template["template"]
        prompt.update()
        return prompt
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.delete("/{alias}", status_code=status.HTTP_200_OK)
def delete_prompt(alias: str):
    """Deletes project from database.

    Args:
        alias (str): prompt alias

    Raises:
        HTTPException.DoesNotExist if alias is not found in table.
    """
    try:
        prompt = PromptTemplate.get(alias)
        prompt.delete()
        return prompt
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt {alias} not found in database",
        )


@router.get("/{alias}", status_code=status.HTTP_200_OK)
def get_prompt(alias: str):
    """Get prompt from database.

    Raises:
        HTTPException: prompt found in table.
    """
    try:
        return PromptTemplate.get(alias)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prompt {alias} not found in database",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("", status_code=status.HTTP_200_OK)
def list_prompts():
    """List all prompts."""
    try:
        return PromptTemplate.scan()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{alias}/generate/model/{model}", status_code=status.HTTP_200_OK)
def generate_text_from_prompt_template(
    alias: str, model: str, values: Dict[str, Any], model_parameters: str = Header(None)
):
    """Generates text using a prompt template with specific model.

    Args:
        alias (str): prompt alias
        model (str): model name
        values (Dict[str, Any]): values to fill in template.
        model_parameters (Dict[str, Any]): Model parameters to override default values.
    """
    try:
        if model_parameters is not None:
            model_parameters = json.loads(model_parameters)
        return F.generate_from_prompt_template(
            alias, model, **values, model_parameters=model_parameters
        )
    except (JSONDecodeError, OutputParserException) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.__class__.__name__ + ": " + str(e),
        )
    except (StrOutputParserTypeError, PromptFieldsMissing) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.__class__.__name__ + ": " + str(e),
        )


@router.post("/{alias}/generate/async/model/{model}", status_code=status.HTTP_200_OK)
def generate_text_from_prompt_template_async(
    alias: str, model: str, values: Dict[str, Any], model_parameters: str = Header(None)
):
    """Generates text using a prompt template with specific model.

    Args:
        alias (str): prompt alias
        model (str): model name
        values (Dict[str, Any]): values to fill in template.
        model_parameters (Dict[str, Any]): Model parameters to override default values.
    """
    if model_parameters is not None:
        model_parameters = json.loads(model_parameters)

    custom_task_id = f"{uuid.uuid4().hex}"

    model_parameters = {k: str(v) for k, v in model_parameters.items()}
    generated = Generated(
        id=custom_task_id,
        status=CeleryStatusTypes.PENDING,
        generation=None,
        error=None,
        timestamp=datetime.now(),
        model=model,
        prompt=alias,
        model_parameters=model_parameters,
    )

    generated.save()

    F.generate_from_prompt_template.apply_async(
        args=[alias, model],
        kwargs={
            "model_parameters": model_parameters,
            "generated_id": custom_task_id,
            **values,
        },
        task_id=custom_task_id,
    )

    return generated


@router.post("/{alias}/generate", status_code=status.HTTP_200_OK)
def generate_text_from_default_model(alias: str, values: Dict[str, Any]):
    """Generates text using a prompt template with default model.

    Args:
        alias (str): prompt alias
        values (Dict[str, Any]): values to fill in template.
    """
    return F.generate_from_default_model(alias, **values)


@router.post("/{alias}/generate/async", status_code=status.HTTP_200_OK)
def generate_text_from_default_model_async(alias: str, values: Dict[str, Any]):
    """Generates text using a prompt template with default model.

    Args:
        alias (str): prompt alias
        values (Dict[str, Any]): values to fill in template.
    """
    custom_task_id = f"{uuid.uuid4().hex}"

    model = settings.DEFAULT_MODELS.get(alias, settings.DEFAULT_MODELS["default"])
    model_parameters = MODELS_TO_PARAMETERS.get(
        model, MODELS_TO_PARAMETERS[ChatModel.GPT4_O_MINI]
    )().model_dump()
    model_parameters = {k: str(v) for k, v in model_parameters.items()}

    generated = Generated(
        id=custom_task_id,
        status=CeleryStatusTypes.PENDING,
        generation=None,
        error=None,
        timestamp=datetime.now(),
        model=model,
        prompt=alias,
        model_parameters=model_parameters,
    )

    generated.save()

    F.generate_from_default_model.apply_async(
        args=[alias],
        kwargs={
            "model_parameters": model_parameters,
            "generated_id": custom_task_id,
            **values,
        },
        task_id=custom_task_id,
    )

    return generated
