"""Projects."""

# Standard Library
from typing import List

# 3rd party libraries
from github.GithubException import UnknownObjectException

# Source
from src.settings import get_settings


settings = get_settings()

access_token = settings.github_credentials.github_token.get_secret_value()

g = Github(access_token)

repo_url = settings.github_credentials.github_url

repo = g.get_repo(repo_url)


router = APIRouter(
    prefix="/v2/projects",
)


@router.post("", status_code=status.HTTP_201_CREATED)
def project_creation(alias: str) -> int:
    """Creates project in Github repository."""
    repo.create_file(alias + "/.gitkeep", "Creating empty folder", "")
    return 200


def project_deletion(alias: str) -> int:
    """Deletes project and sub-prompts in Github repository."""
    try:
        contents = repo.get_contents(alias)
    except UnknownObjectException:
        return 404
    contents = repo.get_contents(alias)
    for content_file in contents:
        if content_file.type == "dir":
            sub_contents = repo.get_contents(content_file.path)
            for sub_content_file in sub_contents:
                repo.delete_file(
                    sub_content_file.path, "Delete file", sub_content_file.sha
                )
        else:
            repo.delete_file(content_file.path, "Delete file", content_file.sha)
    return 200


def get_project(alias: str) -> str:
    """Get project (path) in Github repository."""
    contents = repo.get_contents("")
    for content_file in contents:
        if content_file.type == "dir" and content_file.name == alias:
            return content_file.path


def list_projects() -> List[str]:
    """Retrieves a list of projects (list of folder)."""
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
