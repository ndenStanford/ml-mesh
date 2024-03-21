"""Prompt dynamoDB tables."""

# 3rd party libraries
from dyntastic import Dyntastic
from pydantic import Field

# Source
from src.project.exceptions import ProjectInvalidAlias
from src.settings import get_settings


settings = get_settings()


class Prompt(Dyntastic):
    __table_name__ = "prompt"
    __hash_key__ = "alias"
    __range_key__ = "version"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    template: str
    alias: str
    version: int = 0
    parameters: dict = {}
