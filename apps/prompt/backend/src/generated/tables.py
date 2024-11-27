"""Project dynamoDB tables."""

# Standard Library
import datetime
from typing import Dict, Optional, Type

# 3rd party libraries
from dyntastic import Dyntastic
from dyntastic.exceptions import DoesNotExist
from pydantic import field_validator

# Source
from src.generated.constants import GENERATED_ID_FORBIDDEN_CHARACTERS
from src.generated.exceptions import GeneratedInvalidId, GeneratedNotFound
from src.settings import get_settings


settings = get_settings()


class Generated(Dyntastic):
    """Generated project."""

    __table_name__ = "generated"
    __hash_key__ = "id"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    id: str
    status: str
    generation: Optional[Dict[str, str]] = None
    error: Optional[str] = None
    timestamp: datetime.datetime
    model: str
    prompt: str
    model_parameters: Dict[str, str] = None

    @field_validator("id")
    def validate_id(cls, value) -> str:
        """Validates the id.

        Args:
            value (str): The id to be validated

        Raises:
            GeneratedInvalidId: If the generated if is incorrectly formatted

        Returns:
            str: The validated id
        """
        if (
            value == ""
            or value == "{}"
            or value == '""'
            or any(char in GENERATED_ID_FORBIDDEN_CHARACTERS for char in value)
        ):
            raise GeneratedInvalidId(id=value)
        else:
            return value

    def save(self) -> None:
        """Custom save function."""
        return super(Generated, self).save()

    def update_status(self, status, result=None, error=None):
        """Update status."""
        self.status = status
        self.generation = result
        self.error = error
        self.save()

    def delete(self) -> None:
        """Delete generated from database."""
        return super(Generated, self).delete()

    @classmethod
    def get(
        cls: Type["Generated"],
        hash_key,
        range_key=None,
        *,
        consistent_read: bool = False,
    ) -> "Generated":
        """Subclass the get method to retrieve generated."""
        try:
            result = super(Generated, cls).get(
                hash_key, range_key, consistent_read=consistent_read
            )
        except DoesNotExist:
            raise GeneratedNotFound
        return result
