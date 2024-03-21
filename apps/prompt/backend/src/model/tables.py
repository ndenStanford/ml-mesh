"""Language model dynamoDB tables."""

# 3rd party libraries
from dyntastic import Dyntastic

# Source
from src.settings import get_settings


settings = get_settings()


class LanguageModel(Dyntastic):
    __table_name__ = "model"
    __hash_key__ = "name"
    __table_region__ = settings.AWS_REGION
    __table_host__ = settings.DYNAMODB_HOST

    name: str
    parameters: dict
