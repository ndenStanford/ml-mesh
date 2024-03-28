"""Project."""

# 3rd party libraries
from dyntastic import A
from fastapi import APIRouter, HTTPException, status
from github import Github
from slugify import slugify

# Source
from src.extensions.github import repo
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
def create_project(project: str, alias: str, template: str, parameters: dict = {}):
    """Creates prompt in project.

    Args:
        project (str): project
        alias (str): alias for template.
    """
    project_alias = slugify(project)
    project = Project.safe_get(project_alias)
    # if project does exist, create a new version
    if project is not None:
        try:
            prompt = PromptTemplate(
                alias=alias,
                template=template,
                parameters=parameters,
                project=project.alias,
                sha="",
            )
            F.create_prompt(repo, project, prompt)
            return {"message": "Prompt template created successfully"}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
    else:
        e = ProjectNotFound(alias=project_alias)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
