"""Project dynamoDB tables."""

# Standard Library
from typing import Type, Dict, Any, List, Union

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import field_validator
import datetime


# Source
from src.generated.constants import GENERATED_ID_FORBIDDEN_CHARACTERS
from src.generated.exceptions import GeneratedInvalidId
from src.settings import get_settings


settings = get_settings()


class Generated(Dyntastic):
    """Generated project."""

    __table_name__ = "generated"
    __hash_key__ = "id"
    __table_region__ = settings.AWS_DEFAULT_REGION
    __table_host__ = settings.DYNAMODB_HOST

    id: str
    method: str
    generation: Union[str, Dict]
    timestamp: datetime.datetime
    args: List[Any]
    kwargs: Dict[str, Any]

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
        result = super(Generated, cls).get(
            hash_key, range_key, consistent_read=consistent_read
        )

        return result
