"""Settings."""

# 3rd party libraries
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSettings


class ServingBaseParams(OnclusiveFrozenSettings):
    """Base class implementing the environment variable prefix."""

    model_config = SettingsConfigDict(env_prefix="onclusiveml_serving_")
