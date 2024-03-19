"""Schemas."""

# Standard Library
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel, validator

# Source
from src.prompt.v2.exceptions_v2 import (
    CreationProjectImpossible,
    DeletionProtectedProject,
    ProjectInvalidAlias,
    ProjectNotFound,
    ProjectsNotFound,
    ProjectTokenExceedAlias,
)
from src.prompt.v2.Githubtables import GithubTemplateTable
from src.prompt.v2.projects import (
    get_project,
    list_projects,
    project_creation,
    project_deletion,
)
from src.settings import get_settings


settings = get_settings()


class ProjectTemplateSchema(BaseModel):
    """Project template schema.

    This template leverages python templating to generate
    reusable project.
    """

    id: Optional[str] = None
    alias: Optional[str]

    @validator("alias")
    def validate_alias(cls, value, values):
        """Validates the alias.

        Args:
            value (str): The alias to be validated

        Raises:
            ProjectInvalidAlias: If the template is incorrectly formatted

        Returns:
            str: The validated alias
        """
        if (
            value == ""
            or value == "{}"
            or value == '""'
            or any(char in settings.forbidden_characters for char in value)
        ):
            raise ProjectInvalidAlias(alias=value)

        elif len(value) > 30:
            raise ProjectTokenExceedAlias

        else:
            return value

    def save(self) -> None:
        """Creates a new project."""
        # saves new item in table.
        create_project = project_creation(alias=self.alias)
        if create_project != 200:
            raise CreationProjectImpossible(alias=self.alias)

    def delete(self) -> None:
        """Deletes project from table."""
        project = GithubTemplateTable(
            alias=self.alias,
        )
        if not project:
            raise ProjectNotFound(alias=self.alias)

        else:
            delete_project = project_deletion(alias=self.alias)
            if delete_project != 200:
                raise DeletionProtectedProject(alias=self.alias)

    @classmethod
    def get(
        cls,
        alias: Optional[str] = None,
    ) -> Optional[List[str]]:
        """Returns list of projects.

        Raises:
            ProjectNotFound: if no projects is found
        """
        if alias is None:
            projects = list_projects()
            if projects:
                return projects
            else:
                raise ProjectsNotFound()

        else:
            project = get_project(alias=alias)
            if project:
                return project
