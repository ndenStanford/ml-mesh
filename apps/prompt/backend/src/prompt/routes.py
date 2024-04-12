"""Project."""

# Standard Library
from typing import Any, Dict

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status
from github import Github
from slugify import slugify

# Source
from src.extensions.github import github
from src.project.exceptions import ProjectNotFound
from src.project.tables import Project
from src.prompt import functional as F
from src.prompt.exceptions import (
    DeletionProtectedPrompt,
    PromptInvalidParameters,
    PromptInvalidTemplate,
    PromptModelUnsupported,
    PromptNotFound,
    PromptOutsideTempLimit,
    PromptTokenExceedModel,
    PromptVersionNotFound,
)
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
        project (str): project
        alias (str): alias for template.
    """
    # if project does exist, create a new version
    try:
        project = Project.get(prompt.project)
        prompt.save()
        return prompt
    except DoesNotExist as e:
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
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {alias} not found in database",
        )


@router.get("/{alias}", status_code=status.HTTP_200_OK)
def get_prompt(alias: str):
    """Get prompt from database.

    Raises:
        HTTPException: prompt found in table.
    """
    try:
        return PromptTemplate.get(alias)
    except DoesNotExist as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {alias} not found in database",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.post("/{alias}/generate/model/{model}", status_code=status.HTTP_200_OK)
def generate_text_from_prompt_template(alias: str, model: str, values: Dict[str, Any]):
    """Generates text using a prompt template with specific model.

    Args:
        alias (str): prompt alias
        model (str): model name
        values (Dict[str, Any]): values to fill in template.
    """
    return F.generate_from_prompt_template(alias, model, **values["values"])
