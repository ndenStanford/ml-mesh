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

    model_name: str = "transcript-segmentation"
    model_directory: Union[str, Path] = "."


class HandlerSettings(BaseSettings):
    """API configuration."""

    PROMPT_API: str = "http://prompt-backend:4000"
    prompt_alias: str = "ml-transcript-segmentation"
    INTERNAL_ML_ENDPOINT_API_KEY: str = "1234"
    BETTERSTACK_KEY: str = ""


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    HandlerSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
