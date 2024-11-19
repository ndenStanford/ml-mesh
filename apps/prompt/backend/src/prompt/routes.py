"""Project."""

# Standard Library
import json
from json import JSONDecodeError
from typing import Any, Dict

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, Header, HTTPException, status
from langchain_core.exceptions import OutputParserException

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.generated.exceptions import GeneratedCreationImpossible
from src.generated.tables import Generated
from src.project.tables import Project
from src.prompt import functional as F
from src.prompt.constants import GENERATED, CeleryStatusTypes
from src.prompt.exceptions import PromptFieldsMissing, StrOutputParserTypeError
from src.prompt.tables import PromptTemplate
from src.settings import Prediction, get_settings
from src.worker import celery_app


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
        task = F.generate_from_prompt_template.delay(
            alias, model, **values, model_parameters=model_parameters
        )
        return Prediction(
            task_id=task.id,
            status=CeleryStatusTypes.PENDING,
            generated=None,
            error=None,
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


@router.post("/{alias}/generate", status_code=status.HTTP_200_OK)
def generate_text_from_default_model(alias: str, values: Dict[str, Any]):
    """Generates text using a prompt template with default model.

    Args:
        alias (str): prompt alias
        values (Dict[str, Any]): values to fill in template.
    """
    task = F.generate_from_default_model.delay(alias, **values)
    return Prediction(
        task_id=task.id, status=CeleryStatusTypes.PENDING, generated=None, error=None
    )


@router.get("/status/{task_id}", status_code=status.HTTP_200_OK)
def get_task_status(task_id: str) -> Prediction:
    """Fetch the status or result of a Celery task."""
    response = celery_app.AsyncResult(task_id)
    response_data = {
        "task_id": task_id,
        "status": response.state,
        "generated": None,
        "error": None,
    }

    if response_data["status"] == CeleryStatusTypes.SUCCESS:
        if isinstance(response.result, str):
            response_data["generated"] = {GENERATED: response.result}
        else:
            response_data["generated"] = response.result

        try:
            task_metadata = response.backend.get_task_meta(task_id)
            generated = Generated(
                id=task_id,
                method=task_metadata["name"],
                args=task_metadata["args"],
                kwargs={k: str(v) for k, v in task_metadata["kwargs"].items()},
                timestamp=task_metadata["date_done"],
                generation=response_data["generated"],
            ).save()
        except GeneratedCreationImpossible:
            logger.error(f"Unable to save Generated: {str(generated)}")
    elif response_data["status"] == CeleryStatusTypes.FAILURE:
        response_data["error"] = str(response.result)

    prediction = Prediction(**response_data)
    return prediction
