"""Settings."""

# 3rd party libraries
from pydantic import BaseSettings


class Params(BaseSettings):
    """Base class for all parameter classes in the core library.

    Subclassing from BaseSettings allows for configuring parameters
    via environment variables.
    """

    class Config:
        env_prefix = "onclusiveml_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
