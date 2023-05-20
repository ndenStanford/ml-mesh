"""Data models."""

# Standard Library
import json
from string import Formatter
from typing import List, Optional, Union

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.prompt.exceptions import (
    DeletionProtectedPrompt,
    PromptNotFound,
    PromptVersionNotFound,
)
from src.prompt.tables import PromptTemplateTable
from src.settings import get_settings


settings = get_settings()


class PromptTemplateSchema(BaseModel):
    """Prompt template schema.

    This template leverages python templating to generate
    reusable prompt generators.
    """

    id: Optional[str] = None
    template: str
    alias: str
    version: int = 0
    created_at: Optional[str] = None

    @property
    def variables(self) -> List[str]:
        """Returns the list of template variables."""
        return [p for _, p, _, _ in Formatter().parse(self.template) if p is not None]

    def prompt(self, **kwargs) -> str:
        """Generates the prompt from template."""
        params = {variable: kwargs[variable] for variable in self.variables}
        return self.template.format(**params)

    def save(self) -> "PromptTemplateSchema":
        """Creates a new prompt template or update existing."""
        # saves new item in table.
        prompt = PromptTemplateTable(
            template=self.template,
            alias=self.alias,
            version=self.version,
        )
        prompt.save()
        prompt_dict = json.loads(prompt.to_json())
        return PromptTemplateSchema(
            id=prompt_dict["id"],
            template=prompt_dict["template"],
            alias=prompt_dict["alias"],
            version=prompt_dict["version"],
            created_at=prompt_dict["created_at"],
        )

    def delete(self) -> None:
        """Deletes prompt from table."""
        prompt = self.get(self.alias)

        if prompt is None:
            raise PromptNotFound(alias=self.alias)

        for _, x in settings.LIST_OF_PROMPTS.items():
            if prompt.alias in x[1]:
                raise DeletionProtectedPrompt(alias=self.alias)
        prompt.delete()

    @classmethod
    def get(
        cls,
        alias: Optional[str] = None,
        version: Optional[int] = None,
        raises_if_not_found: bool = False,
    ) -> Optional[Union["PromptTemplateSchema", List["PromptTemplateSchema"]]]:
        """Returns row of the table.

        Raises:

        """
        if alias is None:
            return list(
                map(
                    lambda x: PromptTemplateSchema(**json.loads(x.to_json())),
                    list(PromptTemplateTable.scan()),
                )
            )
        if version is None:
            # if no version specified get the latest.
            query = list(PromptTemplateTable.query(alias, scan_index_forward=False))
        else:
            query = list(
                PromptTemplateTable.query(alias, PromptTemplateTable.version == version)
            )
        if not query:
            if raises_if_not_found:
                if version is None:
                    raise PromptNotFound(alias=alias)
                else:
                    raise PromptVersionNotFound(alias=alias, version=version)
            return None
        return PromptTemplateSchema(**json.loads(query[0].to_json()))

    def update(self, **kwargs) -> "PromptTemplateSchema":
        """Updates table record from latest version."""
        query = list(PromptTemplateTable.query(self.alias, scan_index_forward=False))
        return PromptTemplateSchema(
            template=kwargs.get("template"),
            alias=self.alias,
            version=int(query[0].version) + 1,
        ).save()


class PromptTemplateOutputSchema(BaseModel):
    """Prompt Template output schema"""

    id: Optional[str] = None
    template: str
    created_at: Optional[str] = None
    variables: List[str] = []
    version: int
    alias: str

    @classmethod
    def from_template_schema(
        cls, input: Union[PromptTemplateSchema, List[PromptTemplateSchema]]
    ) -> "PromptTemplateOutputSchema":
        """Converts internal schema to output schema."""
        if isinstance(input, list):
            return list(
                map(
                    lambda x: cls(
                        id=x.id,
                        template=x.template,
                        created_at=x.created_at,
                        variables=x.variables,
                        version=x.version,
                        alias=x.alias,
                    ),
                    input,
                )
            )
        return cls(
            id=input.id,
            template=input.template,
            created_at=input.created_at,
            variables=input.variables,
            version=input.version,
            alias=input.alias,
        )


class PromptTemplateListSchema(BaseModel):
    """List of prompt templates."""

    prompts: List[PromptTemplateOutputSchema] = []
