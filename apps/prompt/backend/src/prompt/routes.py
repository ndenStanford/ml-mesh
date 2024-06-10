"""Project."""

# Standard Library
from typing import Any, Dict

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status

# Internal libraries
from onclusiveml.llms.prompt_validator import PromptInjectionException

# Source
from src.project.tables import Project
from src.prompt import functional as F
from src.prompt.tables import PromptTemplate
from src.settings import get_settings


settings = get_settings()

router = APIRouter(
    prefix="/v2/prompts",
)


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
    alias: str,
    model: str,
    values: Dict[str, Any],
    validate_prompt: bool = False,
):
    """Generates text using a prompt template with specific model.

    Args:
        alias (str): prompt alias
        model (str): model name
        values (Dict[str, Any]): values to fill in template.
        validate_prompt (bool): flag to validate prompt
    """
    try:
        return F.generate_from_prompt_template(alias, model, validate_prompt, **values)
    except PromptInjectionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{alias}/generate", status_code=status.HTTP_200_OK)
def generate_text_from_default_model(
    alias: str, values: Dict[str, Any], validate_prompt: bool = False
):
    """Generates text using a prompt template with default model.

    Args:
        alias (str): prompt alias
        values (Dict[str, Any]): values to fill in template.
        validate_prompt (bool): flag to validate prompt
    """
    try:
        return F.generate_from_default_model(alias, validate_prompt, **values)
    except PromptInjectionException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
