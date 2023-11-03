"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "lsh"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
