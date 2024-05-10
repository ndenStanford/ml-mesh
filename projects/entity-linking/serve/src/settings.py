"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import BaseSettings, Field, SecretStr

# Internal libraries
from onclusiveml.serving.params import ServingBaseParams  # noqa
from onclusiveml.serving.rest.serve.params import ServingParams  # noqa
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSpecs,
)
from onclusiveml.core.base.pydantic import OnclusiveBaseSettings


class TrackedTrainedModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("EL-TRAINED-22", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "entity-linking"
    model_directory: Union[str, Path] = "."


class GlobalSettings(
    ServerModelSettings,
    TrackedTrainedModelSpecs,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
