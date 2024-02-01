"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import Union

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import BaseSettings, Field

# Internal libraries
from onclusiveml.serving.params import ServingBaseParams
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import (
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
    TrackedModelSpecs,
)


class TrackedCompiledModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("NER-COMPILED-12", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "ner"
    model_directory: Union[str, Path] = "."


class DownloadSettings(ServingBaseParams):
    """Download settings."""

    wait_seconds_after_download: int = 0


class GlobalSettings(
    ServerModelSettings,
    TrackedCompiledModelSpecs,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> BaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
