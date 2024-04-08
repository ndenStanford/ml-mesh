"""Prompt dynamoDB tables."""

# Standard Library
from typing import Optional

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field

# Source
from src.extensions.github import github
from src.project.exceptions import ProjectInvalidAlias
from src.settings import get_settings


settings = get_settings()


class PromptTemplate(Dyntastic):
    __table_name__ = "prompt"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    template: str
    parameters: dict = {}
    project: str
    sha: Optional[str] = None

    def save(self) -> None:
        """Creates prompt template in github."""
        commit = github.write(
            f"{self.project}/{self.alias}.json",
            f"Add new prompt {self.alias}",
            self.json(exclude={"sha", "project"}),
        )
        self.sha = commit["commit"].sha
        return super(PromptTemplate, self).save()

    def delete(self) -> None:
        """Delete project from database and github."""
        github.rm(os.path.join(project, self.alias), f"Delete prompt {self.alias}")
        return super(Project, self).delete()
