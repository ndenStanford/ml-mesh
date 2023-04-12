"""Data models."""

# Standard Library
import json
from string import Formatter
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.model.tables import ModelTable


class ModelSchema(BaseModel):
    """Model schema."""

    id: Optional[str] = None
    model: str
    created_at: Optional[str] = None

    @property
    def variables(self) -> List[str]:
        """Returns the list of model variables."""
        return [p for _, p, _, _ in Formatter().parse(self.model) if p is not None]

    def model(self, **kwargs) -> str:
        """Generates the model name."""
        params = {variable: kwargs[variable] for variable in self.variables}
        return self.model.format(**params)

    def save(self) -> "ModelSchema":
        """Creates a new model or update existing."""
        # saves new item in table.
        model = ModelTable(
            model=self.model,
        )
        model.save()
        model_dict = json.loads(model.to_json())
        return ModelSchema(
            id=model_dict["id"],
            model=model_dict["model"],
            created_at=model_dict["created_at"],
        )

    @classmethod
    def get(cls, id: Optional[str] = None) -> "ModelSchema":
        """Returns row of the table."""
        if id is None:
            return list(
                map(
                    lambda x: ModelSchema(**json.loads(x.to_json())),
                    list(ModelTable.scan()),
                )
            )
        return ModelSchema(**json.loads(ModelTable.get(id).to_json()))

    def update(self, **kwargs) -> None:
        """Updates table record."""
        model = ModelTable.get(self.id)
        model.update(actions=[ModelTable.model.set(kwargs.get("model"))])


class ModelListSchema(BaseModel):
    """List of models."""

    models: List[ModelSchema] = []
