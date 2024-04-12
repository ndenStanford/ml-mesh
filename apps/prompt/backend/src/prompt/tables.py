"""Prompt dynamoDB tables."""

# Standard Library
import os
from typing import Optional, Type

# 3rd party libraries
from boto3.dynamodb.conditions import ConditionBase
from dyntastic import A, Dyntastic
from dyntastic.main import ResultPage
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
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
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    alias: str
    template: str
    project: str
    sha: Optional[str] = None

    @property
    def path(self) -> str:
        """Prompt file path."""
        return os.path.join(self.project, f"{self.alias}.json")

    def save(self) -> None:
        """Creates prompt template in github."""
        commit = github.write(
            self.path,
            f"Add new prompt {self.alias}",
            self.json(exclude={"sha", "project", "alias"}),
        )
        self.sha = commit["commit"].sha
        return super(PromptTemplate, self).save()

    def delete(self) -> None:
        """Delete project from database and github."""
        github.rm(self.path, f"Delete prompt {self.alias}")
        return super(PromptTemplate, self).delete()

    def as_langchain(self) -> Optional[LangchainT]:
        """Convert to langchain object."""
        return ChatPromptTemplate.from_messages(
            [HumanMessagePromptTemplate.from_template(self.template)]
        )

    @classmethod
    def get(cls: Type["PromptTemplate"], hash_key, range_key=None) -> "PromptTemplate":
        """Subclass the get method to retrieve templates directly from Github."""
        result = super(PromptTemplate, cls).get(hash_key, range_key)
        print(result)
        # get template from github
        contents = github.read(result.path)
        # use the github template as the source of truth.
        result.template = contents["template"]
        return result

    @classmethod
    def scan(
        cls: Type["PromptTemplate"],
        project: Optional[str] = None,
    ) -> ResultPage["PromptTemplate"]:
        """Subclass the scan method to retrieve templates directly from Github."""
        if project is None:
            return super(PromptTemplate, cls).scan()
        results = list(
            super(PromptTemplate, cls).scan(
                (A.project.is_in([project])), consistent_read=True
            )
        )
        for result in results:
            # get from github
            contents = github.read(result.path)
            # use the github template as the source of truth.
            result.template = contents["template"]

        return results
