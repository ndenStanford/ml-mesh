"""Project functionals."""

# Standard Library
from typing import Any, List


def create_project(repo: Any, alias: str) -> None:
    """Creates project in Github repository."""
    repo.create_file(alias + "/.gitkeep", f"Creating project {alias}", "")


def delete_project(repo: Any, alias: str) -> None:
    """Deletes project and sub-prompts in Github repository."""
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


def get_project(repo: Any, alias: str) -> str:
    """Get project (path) in Github repository."""
    contents = repo.get_contents("")
    for content_file in contents:
        if content_file.type == "dir" and content_file.name == alias:
            return content_file.path


def list_projects() -> List[str]:
    """Retrieves a list of projects (list of folder)."""
    contents = repo.get_contents("")
    projects = list_folders_recursive(contents)
    return projects


def list_folders_recursive(contents, path="") -> List[str]:
    """Recursively list folders."""
    projects = []
    for content_file in contents:
        if content_file.type == "dir":
            projects.append(content_file.name)
            sub_contents = repo.get_contents(content_file.path)
            projects.extend(list_folders_recursive(sub_contents))
    return projects
