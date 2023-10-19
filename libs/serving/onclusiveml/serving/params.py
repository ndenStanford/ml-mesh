"""Settings."""

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSettings


class ServingBaseParams(OnclusiveFrozenSettings):
    """Base class implementing the environment variable prefix."""

    class Config:
        env_prefix = "onclusiveml_serving_"
        env_file_encoding = "utf-8"
