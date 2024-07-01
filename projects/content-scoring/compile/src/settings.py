"""Settings."""

# Standard Library
from typing import List

# Internal libraries
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


class CompiledTrackedModelSettings(TrackingSettings):
    """Tracked specifications for a compiled model.

    Attributes:
        project (str): The project name for the model
        model (str): The model name
    """

    target_model: str = "NER-COMPILED"


class ModelTracingSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.compiled_model.compile_model for details.

    This should be refactored to not cause issues with torch.jit.trace anymore. See ticket
    https://onclusive.atlassian.net/browse/DS-596

    Attributes:
        dynamic_batch_size (bool): Flag for using dynamic batch size
        strict (bool): Flag for strict compilation
        compiler_args (List[str]): List of compiler arguments
    """

    dynamic_batch_size: bool = True
    strict: bool = False
    compiler_args: List[str] = ["--fast-math", "none"]


class CompiledContentScoringTrackedModelCard(TrackedModelCard):
    """Compiled content-scoring tracked model card."""

    model_type: str = "compiled"

    uncompiled_model: UncompiledTrackedModelSettings = UncompiledTrackedModelSettings()


class GlobalSettings(
    TrackedModelSettings,
    OnclusiveLogSettings,
    CompiledTrackedModelSettings,
    ModelTracingSettings,
    CompiledContentScoringTrackedModelCard,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
