"""Projects."""

# 3rd party libraries
from dyntastic.exceptions import DoesNotExist
from fastapi import APIRouter, HTTPException, status

# Source
from src.project.exceptions import ProjectsExisting
from src.project.tables import Project
from src.prompt.tables import PromptTemplate


router = APIRouter(
    prefix="/v2/projects",
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(alias: str):
    """Creates project.

    Args:
        alias (str): alias for template.
    """
    project = Project.safe_get(alias)
    # if project does exist, create a new version
    if project is None:
        try:
            Project(alias=alias).save()
            return Project(alias=alias)

        except HTTPException as e:
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
    try:
        project = Project.get(alias)
        project.delete()
        return project
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {alias} not found in database",
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
def get_project(alias: str):
    """Get project from database.

    Raises:
        HTTPException.ProjectNotFound named project found in table.
    """
    try:
        return Project.get(alias)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {alias} not found in database",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{alias}/prompts", status_code=status.HTTP_200_OK)
def list_prompts(alias: str):
    """Get list of projects from database.

    Raises:
        HTTPException.ProjectsNotFound if no projects found in table.
    """
    try:
        return PromptTemplate.scan(alias)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
