"""Settings."""

# Standard Library
from functools import lru_cache

# Internal libraries
from onclusiveml.core.base import OnclusiveFrozenSettings
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "transcript-segmentation"


class PromptBackendAPISettings(OnclusiveFrozenSettings):
    """API configuration."""

    prompt_api_url: str = "http://prompt-backend:4000"
    prompt_alias: str = "ml-transcript-segmentation"
    internal_ml_endpoint_api_key: str = "1234"
    CHARACTER_BUFFER: int = 2500


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveFrozenSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()


@lru_cache
def get_api_settings() -> OnclusiveFrozenSettings:
    """Returns API settings."""
    return PromptBackendAPISettings()
