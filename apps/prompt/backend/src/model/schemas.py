"""Data models."""

# Standard Library
import json
from typing import List, Optional

# 3rd party libraries
from pydantic import BaseModel

# Source
from src.model.tables import ModelTable
from src.settings import get_settings


settings = get_settings()


class ModelSchema(BaseModel):
    """Model schema."""

    id: Optional[str] = None
    model_name: str
    created_at: Optional[str] = None
    parameters: Optional[str] = json.dumps(
        {
            "max_tokens": settings.OPENAI_MAX_TOKENS,
            "temperature": settings.OPENAI_TEMPERATURE,
        }
    )

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

    def get_model_name(self) -> str:
        """Returns the model name."""
        return self.model_name


class ModelListSchema(BaseModel):
    """List of models."""

    models: List[ModelSchema] = []
