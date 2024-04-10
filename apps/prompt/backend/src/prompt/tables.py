"""Prompt dynamoDB tables."""

# Standard Library
from typing import Optional

# 3rd party libraries
from dyntastic import Dyntastic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from pydantic import Field

# Internal libraries
from onclusiveml.llm.mixins import LangchainConvertibleMixin
from onclusiveml.llm.typing import LangchainT

# Source
from src.extensions.github import github
from src.project.exceptions import ProjectInvalidAlias
from src.settings import get_settings


settings = get_settings()


class PromptTemplate(Dyntastic, LangchainConvertibleMixin):
    __table_name__ = "prompt"
    __hash_key__ = "alias"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    template: str
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

    def as_langchain(self) -> Optional[LangchainT]:
        """Convert to langchain object."""
        return ChatPromptTemplate.from_messages(
            [HumanMessagePromptTemplate.from_template(self.template)]
        )
