# 3rd party libraries
from pydantic import BaseSettings


class ServingBaseParams(BaseSettings):
    """Base class implementing the environment variable prefix"""

    class Config:
        env_prefix = "onclusiveml_serving_"
        env_file_encoding = "utf-8"