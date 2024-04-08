"""Project."""

# Standard Library
from typing import Any, Dict

# 3rd party libraries
from dyntastic import A
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status
from github import Github
from slugify import slugify

# Source
from src.extensions.github import github
from src.project.exceptions import ProjectNotFound
from src.project.tables import Project
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


@router.get("/project/{project}", status_code=status.HTTP_200_OK)
def list_prompts(project: str):
    """Get list of projects from database.

    Raises:
        HTTPException.ProjectsNotFound if no projects found in table.
    """
    try:
        return PromptTemplate.scan((A.project == project))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
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
def generate_with_diff_model(alias: str, model: str, values: Dict[str, Any]):
    """Generates text using a prompt template.

    Args:
        alias (str): prompt alias
        model_name (str): model name
        values (Dict[str, Any]): values to fill in template.
    """


@router.post("/generate", status_code=status.HTTP_200_OK)
def generate_text_from_chat(values):
    """Retrieves prompt via id.

    Args:
        values (Dict[str, Any]): input from chat
    """


@router.post("/generate/model/{model}", status_code=status.HTTP_200_OK)
def generate_text_from_chat_diff_model(model: str, values):
    """Retrieves prompt via id.

    Args:
        values (Dict[str, Any]): input from chat
        model_name (str): model name
    """
