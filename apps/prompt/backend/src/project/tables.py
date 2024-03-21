"""Project dynamoDB tables."""

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field

# Source
from src.project.exceptions import ProjectInvalidAlias
from src.settings import get_settings


settings = get_settings()


class Project(Dyntastic):
    __table_name__ = "project"
    __hash_key__ = "id"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    alias: str

    @validator("alias")
    def validate_alias(cls, value, values):
        """Validates the alias.

        Args:
            value (str): The alias to be validated

        Raises:
            ProjectInvalidAlias: If the template is incorrectly formatted

        Returns:
            str: The validated alias
        """
        if (
            value == ""
            or value == "{}"
            or value == '""'
            or any(char in settings.forbidden_characters for char in value)
        ):
            raise ProjectInvalidAlias(alias=value)

        elif len(value) > 30:
            raise ProjectTokenExceedAlias

        else:
            return value
