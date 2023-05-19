# 3rd party libraries
from pydantic import BaseSettings


class Params(BaseSettings):

    """Base class for all parameter classes in the core library. Subclassing from BaseSettings
    allows for configuring parameters via environment variables."""

    pass
