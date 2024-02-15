"""Prompt."""

# Standard Library
from typing import List

# 3rd party libraries
from fastapi import APIRouter, HTTPException, status
from github import Github

# Source
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
def create_project(folder_path: str):
    """Creates a new project folder."""
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
    """Deletes a project folder."""
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


@router.get("", status_code=status.HTTP_200_OK, response_model=List[str])
def list_projects():
    """Retrieves a list of projects."""
    try:
        contents = repo.get_contents("")
        projects = list_folders_recursive(contents)
        return projects
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


def list_folders_recursive(contents, path="") -> List[str]:
    """Recursively list folders."""
    projects = []
    for content_file in contents:
        if content_file.type == "dir":
            projects.append(content_file.name)
            sub_contents = repo.get_contents(content_file.path)
            projects.extend(list_folders_recursive(sub_contents))
    return projects
