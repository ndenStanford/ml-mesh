"""Data models."""

# Standard Library
import json
from string import Formatter
from typing import List, Optional, Union

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.prompt.tables import PromptTemplateTable


class PromptTemplateSchema(BaseModel):
    """Prompt template schema.

    This template leverages python templating to generate
    reusable prompt generators.
    """

    id: Optional[str] = None
    template: str
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
        )
        prompt.save()
        prompt_dict = json.loads(prompt.to_json())
        return PromptTemplateSchema(
            id=prompt_dict["id"],
            template=prompt_dict["template"],
            created_at=prompt_dict["created_at"],
        )

    @classmethod
    def get(
        cls, id: Optional[str] = None
    ) -> Union["PromptTemplateSchema", List["PromptTemplateSchema"]]:
        """Returns row of the table."""
        if id is None:
            return list(
                map(
                    lambda x: PromptTemplateSchema(**json.loads(x.to_json())),
                    list(PromptTemplateTable.scan()),
                )
            )
        return PromptTemplateSchema(**json.loads(PromptTemplateTable.get(id).to_json()))

    def update(self, **kwargs) -> None:
        """Updates table record."""
        prompt = PromptTemplateTable.get(self.id)
        prompt.update(
            actions=[PromptTemplateTable.template.set(kwargs.get("template"))]
        )


class PromptTemplateOutputSchema(BaseModel):
    """Prompt Template output schema"""

    id: Optional[str] = None
    template: str
    created_at: Optional[str] = None
    variables: List[str] = []

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
                    ),
                    input,
                )
            )
        return cls(
            id=input.id,
            template=input.template,
            created_at=input.created_at,
            variables=input.variables,
        )


class PromptTemplateListSchema(BaseModel):
    """List of prompt templates."""

    prompts: List[PromptTemplateOutputSchema] = []
