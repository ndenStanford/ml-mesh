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
    model_name: str
    created_at: Optional[str] = None

    def save(self) -> "ModelSchema":
        """Creates a new model or update existing."""
        # saves new item in table.
        model = ModelTable(
            model_name=self.model_name,
        )
        model.save()
        model_dict = json.loads(model.to_json())
        return ModelSchema(
            id=model_dict["id"],
            model_name=model_dict["model_name"],
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
        model.update(actions=[ModelTable.model_name.set(kwargs.get("model_name"))])

    def get_model_name(self) -> str:
        """Returns the model name."""
        return self.model_name


class ModelListSchema(BaseModel):
    """List of models."""

    models: List[ModelSchema] = []
