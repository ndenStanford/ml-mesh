"""Settings."""

# Standard Library
import os
from functools import lru_cache
from typing import Dict, List

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.compile.constants import CompileWorkflowTasks
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import OnclusiveLogSettings
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackingSettings,
)


class ModelTrackedSettings(TrackedModelSettings):
    """Models settings."""

    compiled_model: str
    mode: str = Field(Mode.READ_ONLY)


class IOSettings(TrackingSettings):
    """Configuring container file system output locations for all 4 components."""

    base_path: str

    model_config = SettingsConfigDict(env_prefix="io_settings_")

    def output_directory(self, task: CompileWorkflowTasks) -> str:
        """Output directory for task."""
        output_directory: str = os.path.join("models", self.base_path, task)
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)
        return output_directory

    def model_directory(self, task: CompileWorkflowTasks) -> str:
        """Returns model directory given task."""
        return os.path.join(self.output_directory(task), "model_artifacts")

    def test_files(self, task: CompileWorkflowTasks) -> Dict[str, str]:
        """Test files location."""
        return {
            "inputs": os.path.join(self.output_directory(task), "inputs.json"),
            "inference_params": os.path.join(
                self.output_directory(task),
                "inference_params.json",
            ),
            "predictions": os.path.join(
                self.output_directory(task), "predictions.json"
            ),
        }


class TokenizerSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.tokenizer for details."""

    add_special_tokens: bool = True

    model_config = SettingsConfigDict(env_prefix="tokenizer_settings_")


class ModelTracingSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.model.compile_model for details.

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

    model_config = SettingsConfigDict(env_prefix="model_tracing_settings_")


class PipelineCompilationSettings(TrackingSettings):
    """Pipeline compilation settings."""

    word_pipeline_max_length: int
    document_pipeline_max_length: int
    batch_size: int = 1
    neuron: bool = True
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = 1e-02

    model_config = SettingsConfigDict(env_prefix="pipeline_compilation_settings_")


class CompilationTestSettings(TrackingSettings):
    """Compilation test settings."""

    regression_atol: float = 1e-02
    regression_rtol: float = 1e-02

    model_config = SettingsConfigDict(env_prefix="compilation_test_settings_")


class TrackedModelCard(TrackedModelCard):
    """Model card."""

    model: ModelTrackedSettings = ModelTrackedSettings()
    compilation_test_settings: CompilationTestSettings = CompilationTestSettings()


class GlobalSettings(
    ModelTrackedSettings,
    IOSettings,
    TokenizerSettings,
    ModelTracingSettings,
    PipelineCompilationSettings,
    CompilationTestSettings,
    OnclusiveLogSettings,
):
    """Global server settings."""

    model_card: TrackedModelCard = TrackedModelCard()


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
