"""Settings."""

# Standard Library
from functools import lru_cache
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from pydantic import BaseSettings

# Internal libraries
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "iptc-multi"
    model_directory: Union[str, Path] = "."
    max_topic_num: int = 5
    min_score_cutoff: float = 0.01
    model_endpoint_template: str = "serve-iptc-{}:8000"
    model_endpoint_secure: bool = False
    test_model_sequence: List[str] = []

    class Config:
        env_prefix = "server_model_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


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
