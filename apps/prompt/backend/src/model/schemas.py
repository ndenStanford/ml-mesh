"""Data models."""

# Standard Library
import datetime
import json
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.model.exceptions import ModelNotFound
from src.model.tables import ModelTable
from src.settings import get_settings


settings = get_settings()


class ModelSchema(BaseModel):
    """Model schema."""

    id: Optional[str] = None
    model_name: str
    created_at: Optional[datetime.datetime] = None
    parameters: Optional[str] = None

    def save(self) -> "ModelSchema":
        """Creates a new model or update existing."""
        # saves new item in table.
        model = ModelTable(
            model_name=self.model_name,
            parameters=self.parameters,
        )
        model.save()
        model_dict = json.loads(model.to_json())
        return ModelSchema(
            id=model_dict["id"],
            model_name=model_dict["model_name"],
            created_at=model_dict["created_at"],
            parameters=model_dict["parameters"],
        )

    @classmethod
    def get(
        cls, model_name: Optional[str] = None, raises_if_not_found: bool = False
    ) -> Optional["ModelSchema"]:
        """Returns row of the table."""
        if model_name is None:
            return list(
                map(
                    lambda x: ModelSchema(**json.loads(x.to_json())),
                    list(ModelTable.scan()),
                )
            )
        model = ModelTable.query(model_name)
        model = list(model)
        if not model:
            if raises_if_not_found:
                raise ModelNotFound(model_name=model_name)
            return None
        model = model[0]
        return cls(
            id=model.id,
            model_name=model.model_name,
            created_at=model.created_at,
            parameters=model.parameters,
        )

    def get_model_name(self) -> str:
        """Returns the model name."""
        return self.model_name


class ModelListSchema(BaseModel):
    """List of models."""

    models: List[ModelSchema] = []
