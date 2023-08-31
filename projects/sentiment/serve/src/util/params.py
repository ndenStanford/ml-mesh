"""Settings."""

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import TrackedModelSpecs

# Source
from src.params import ServedModelParams  # noqa: F401


class TrackedCompiledModelSpecs(TrackedModelSpecs):
    """Tracked compiled model settings."""

    # project: str = "onclusive/sentiment"
    # model: str = "SEN-TRAINED"

    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = Field("SEN-COMPILED-12", env="neptune_model_version_id")
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY, env="neptune_client_mode")
