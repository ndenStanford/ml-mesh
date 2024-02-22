"""Project."""

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status
from github import Github
from slugify import slugify

# Source
from src.prompt.exceptions_v2 import (
    DeletionProtectedProject,
    ProjectNotFound,
    ProjectsExisting,
)
from src.prompt.schemas_v2 import ProjectTemplateSchema
from src.settings import get_settings


settings = get_settings()

router = APIRouter(
    prefix="/v2/prompts",
)

access_token = settings.github_credentials.github_token.get_secret_value()

g = Github(access_token)

repo_url = settings.github_credentials.github_url

repo = g.get_repo(repo_url)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(alias: str):
    """Creates project.

    Args:
        alias (str): alias for template.
    """
    alias = slugify(alias)
    project = ProjectTemplateSchema.get(alias)
    # if project does exist, create a new version
    if not project:
        try:
            ProjectTemplateSchema(alias=alias).save()
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
    project = ProjectTemplateSchema.get(alias)
    if not project:
        e = ProjectNotFound(alias=alias)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    else:
        try:
            ProjectTemplateSchema(alias=alias).delete()
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
        projects = ProjectTemplateSchema().get()
        return projects
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
        project = ProjectTemplateSchema(alias=alias).get(alias=alias)
        if not project:
            raise ProjectNotFound(alias=alias)
        else:
            return project
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


"""
@router.get("", status_code=status.HTTP_200_OK, response_model=List[str])
def list_projects():
    try:
        contents = repo.get_contents("")
        projects = list_folders_recursive(contents)
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

@router.post("", status_code=status.HTTP_201_CREATED)
def create_project(folder_path: str):
    try:
        repo.create_file(folder_path + "/.gitkeep", "Creating empty folder", "")
        return {"message": "Project created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.delete("/{folder_path}", status_code=status.HTTP_200_OK)
def delete_project(folder_path: str):
    try:
        contents = repo.get_contents(folder_path)

        for content_file in contents:
            if content_file.type == "dir":
                sub_contents = repo.get_contents(content_file.path)
                for sub_content_file in sub_contents:
                    repo.delete_file(
                        sub_content_file.path, "Delete file", sub_content_file.sha
                    )
            else:
                repo.delete_file(content_file.path, "Delete file", content_file.sha)

        return {"message": "Project deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
"""
