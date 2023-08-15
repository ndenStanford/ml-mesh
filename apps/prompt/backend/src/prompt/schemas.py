"""Data models."""

# Standard Library
import datetime
import json
from string import Formatter
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel, validator

# Source
from src.prompt.exceptions import (
    DeletionProtectedPrompt,
    PromptInvalidTemplate,
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
    created_at: Optional[datetime.datetime] = None

    @validator("template")
    def validate_template(cls, value, values):
        if value == "" or value == "{}" or value == '""':
            raise PromptInvalidTemplate(template=value)
        else:
            # Test template using formatter. Raise error if incorrectly formatted
            try:
                [i[1] for i in Formatter().parse(value) if i[1] is not None]
            except ValueError:
                raise PromptInvalidTemplate(template=value)
            return value

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
        prompts = PromptTemplateTable.query(self.alias, scan_index_forward=False)

        prompts = list(prompts)

        if not prompts:
            raise PromptNotFound(alias=self.alias)

        for prompt in prompts:
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
    ) -> Optional[List["PromptTemplateSchema"]]:
        """Returns row of the table.

        Note: returns a list even when the

        Raises:
            PromptNotFound: of
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
            query = PromptTemplateTable.query(alias, scan_index_forward=False)
        else:
            query = PromptTemplateTable.query(
                alias, PromptTemplateTable.version == version
            )

        query = list(query)

        if not query:
            if raises_if_not_found:
                if version is None:
                    raise PromptNotFound(alias=alias)
                else:
                    raise PromptVersionNotFound(alias=alias, version=version)
            return None

        return list(
            map(
                lambda x: cls(
                    id=x.id,
                    template=x.template,
                    created_at=x.created_at,
                    version=x.version,
                    alias=x.alias,
                ),
                query,
            )
        )

    def update(self, **kwargs) -> "PromptTemplateSchema":
        """Updates table record from latest version."""
        query = list(PromptTemplateTable.query(self.alias, scan_index_forward=False))
        updated_template = PromptTemplateSchema(
            template=kwargs.get("template"),
            alias=self.alias,
            version=int(query[0].version) + 1,
        )
        return updated_template.save()


class PromptTemplateOutputSchema(BaseModel):
    """Prompt Template output schema"""

    id: Optional[str] = None
    template: str
    created_at: Optional[datetime.datetime] = None
    variables: List[str] = []
    version: int
    alias: str

    @classmethod
    def from_template_schema(
        cls, input: List[PromptTemplateSchema]
    ) -> List["PromptTemplateOutputSchema"]:
        """Converts internal schema to output schema."""
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


class PromptTemplateListSchema(BaseModel):
    """List of prompt templates."""

    prompts: List[PromptTemplateOutputSchema] = []
