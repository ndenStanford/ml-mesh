"""Projects."""

# Standard Library
from typing import List

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status
from github.GithubException import UnknownObjectException
from slugify import slugify

# Source
from src.extensions.github import repo
from src.project import functional as F
from src.project.exceptions import (
    CreationProjectImpossible,
    DeletionProtectedProject,
    ProjectInvalidAlias,
    ProjectNotFound,
    ProjectsExisting,
    ProjectsNotFound,
    ProjectTokenExceedAlias,
)
from src.project.tables import Project
from src.settings import get_settings


router = APIRouter(
    prefix="/v2/projects",
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(alias: str):
    """Creates project.

    Args:
        alias (str): alias for template.
    """
    alias = slugify(alias)
    project = Project.safe_get(alias)
    # if project does exist, create a new version
    if project is None:
        try:
            Project(alias=alias).save()
            F.create_project(repo, alias)
            return {"message": "Project created successfully"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(e),
            )
    else:
        e = ProjectsExisting(alias=alias)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.delete("/{alias}", status_code=status.HTTP_200_OK)
def delete_project(alias: str):
    """Deletes project from database.

    Args:
        alias (str): prompt alias

    Raises:
        HTTPException.DoesNotExist if alias is not found in table.
    """
    alias = slugify(alias)
    project = Project.get(alias)
    if not project:
        e = ProjectNotFound(alias=alias)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    else:
        try:
            Project(alias=alias).delete()
            F.delete_project(repo, alias)
            return {"message": "Project deleted successfully"}
        except ProjectNotFound as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        except DeletionProtectedProject as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e),
            )


@router.get("", status_code=status.HTTP_200_OK)
def list_projects():
    """Get list of projects from database.

    Raises:
        HTTPException.ProjectsNotFound if no projects found in table.
    """
    try:
        return Project.scan()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{alias}", status_code=status.HTTP_200_OK)
def get_projects(alias: str):
    """Get project from database.

    Raises:
        HTTPException.ProjectNotFound named project found in table.
    """
    try:
        project = Project.get(alias)
        if not project:
            raise ProjectNotFound(alias=alias)
        else:
            return project
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
