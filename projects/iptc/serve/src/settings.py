"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

# 3rd party libraries
from neptune.types.mode import Mode

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import OnclusiveLogSettings
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSettings,
)


class ServerModelSettings(ServingParams):
    """Prediction model settings."""

    model_name: str
    model_directory: Union[str, Path] = "."


class IPTCTrackedModelSettings(TrackedModelSettings):
    """Tracked compiled model settings."""

    mode: str = Mode.READ_ONLY


class GlobalSettings(
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    ServerModelSettings,
    IPTCTrackedModelSettings,
    OnclusiveLogSettings,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
