"""Settings."""

# Standard Library
from functools import lru_cache
from typing import List

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import OnclusiveLogSettings
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


class TokenizerSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.compiled_tokenizer for details.

    Attributes:
        add_special_tokens (bool): Flag for adding special tokens
    """

    add_special_tokens: bool


class ModelTracingSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.compiled_model.compile_model for details.

    This should be refactored to not cause issues with torch.jit.trace anymore. See ticket
    https://onclusive.atlassian.net/browse/DS-596

    Attributes:
        dynamic_batch_size (bool): Flag for using dynamic batch size
        strict (bool): Flag for strict compilation
        compiler_args (List[str]): List of compiler arguments
    """

    dynamic_batch_size: bool
    strict: bool
    compiler_args: List[str] = ["--fast-math", "none"]


class PipelineCompilationSettings(TrackingSettings):
    """See libs.compile.onclusiveml.compile.compiled_pipeline.compile_pipeline for details.

    Attributes:
        pipeline_name (str): Name of pipeline
        max_length (int): max sequence length:
        batch_size (int): Batch size for compilation
        neuron (bool): Flag for neuron compilation
        validate_compilation (bool): Flag for running validation tests
        validation_rtol (float): Relative tolerance for validation
        validation_atol (float): Absolute tolerance for validation
        tokenizer_settings (TokenizerSettings): settings for tokenizer
        model_tracing_settings (ModelTracingSettings): Settings for model tracing

    """

    pipeline_name: str
    max_length: int
    batch_size: int
    neuron: bool
    validate_compilation: bool
    validation_rtol: float
    validation_atol: float
    tokenizer_settings: TokenizerSettings = TokenizerSettings()
    model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class NERPipelineCompilationSettings(PipelineCompilationSettings):
    """Tracked model card for a compiled NER model.

    Attributes:
        pipeline_name (str): Name of the NER pipeline
        max_length (int): Max sequence length for NER
    """

    pipeline_name: str
    max_length: int


class CompilationTestSettings(TrackingSettings):
    """Settings for compilation tests.

    Attributes:
        regression_atol (float): Relative tolerance for validation
        regression_rtol (float): Absolute tolerance for validation
    """

    regression_atol: float
    regression_rtol: float


class CompiledNERTrackedModelCard(TrackedModelCard):
    """Tracked model card for a compiled NER model.

    Attributes:
        model_type(str): Type of the model card
        uncompiled_model (TrackedModelSettings): Specifications for the uncompiled model
        ner_model_compilation_settings (PipelineCompilationSettings): Compilation settings
        compilation_test_settings (CompilationTestSettings): Compilation test settings
    """

    model_type: str = "compiled"
    # --- custom fields
    files: List[str] = [
        "base_ner",
        "korean_japanese_ner",
    ]
    test_files: List[str] = []
    # uncompiled model reference
    uncompiled_model: TrackedModelSettings = TrackedModelSettings()
    # model compilation params
    ner_model_compilation_settings: PipelineCompilationSettings = (
        NERPipelineCompilationSettings()
    )

    compilation_test_settings: CompilationTestSettings = CompilationTestSettings()


class GlobalSettings(
    TrackedModelSettings,
    OnclusiveLogSettings,
    CompiledTrackedModelSettings,
    TokenizerSettings,
    ModelTracingSettings,
    NERPipelineCompilationSettings,
    CompilationTestSettings,
    CompiledNERTrackedModelCard,
):
    """Global server settings."""


@lru_cache
def get_settings() -> OnclusiveBaseSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()
