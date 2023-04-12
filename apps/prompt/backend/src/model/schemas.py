"""Data models."""

# Standard Library
import json
from string import Formatter
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.model.tables import ModelTemplateTable


class ModelTemplateSchema(BaseModel):
    """Model template schema.

    s"""

    id: Optional[str] = None
    template: str
    created_at: Optional[str] = None

    @property
    def variables(self) -> List[str]:
        """Returns the list of template variables."""
        return [p for _, p, _, _ in Formatter().parse(self.template) if p is not None]

    def model(self, **kwargs) -> str:
        """Generates the model from template."""
        params = {variable: kwargs[variable] for variable in self.variables}
        return self.template.format(**params)

    def save(self) -> "ModelTemplateSchema":
        """Creates a new model template or update existing."""
        # saves new item in table.
        model = ModelTemplateTable(
            template=self.template,
        )
        model.save()
        model_dict = json.loads(model.to_json())
        return ModelTemplateSchema(
            id=model_dict["id"],
            template=model_dict["template"],
            created_at=model_dict["created_at"],
        )

    @classmethod
    def get(cls, id: Optional[str] = None) -> "ModelTemplateSchema":
        """Returns row of the table."""
        if id is None:
            return list(
                map(
                    lambda x: ModelTemplateSchema(**json.loads(x.to_json())),
                    list(ModelTemplateTable.scan()),
                )
            )
        return ModelTemplateSchema(**json.loads(ModelTemplateTable.get(id).to_json()))

    def update(self, **kwargs) -> None:
        """Updates table record."""
        model = ModelTemplateTable.get(self.id)
        model.update(actions=[ModelTemplateTable.template.set(kwargs.get("template"))])


class ModelTemplateListSchema(BaseModel):
    """List of model templates."""

    models: List[ModelTemplateSchema] = []
