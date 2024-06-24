"""Settings."""

# Standard Library
import os
from typing import List

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.core.logging import INFO
from onclusiveml.tracking import (
    TrackedModelCard,
    TrackedModelSettings,
    TrackedParams,
)


# --- atomic settings and models
DOWNLOAD = "download"
COMPILE = "compile"
TEST = "test"
UPLOAD = "upload"
WORKFLOW_COMPONENTS = (DOWNLOAD, COMPILE, TEST, UPLOAD)


class UncompiledTrackedModelSettings(TrackedModelSettings):
    """Trained model settings."""

    project: str = "onclusive/sentiment"
    model: str = "SEN-TRAINED"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "SEN-TRAINED-37"
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)

    class Config:
        env_prefix = "uncompiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledTrackedModelSettings(TrackedModelSettings):
    """Compiled model settings."""

    project: str = "onclusive/sentiment"
    model: str = "SEN-COMPILED"

    class Config:
        env_prefix = "compiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowOutputDir(TrackedParams):
    """Workflow output directory."""

    outpath: str = "./outputs"

    class Config:
        env_prefix = "compiled_pipeline_io_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowComponentIOSettings(object):
    """Workflow component IO settings."""

    workflow_ouput_dir: str = WorkflowOutputDir().outpath

    def __init__(self, workflow_component: str):
        self.check_component_reference(workflow_component)

        self.workflow_component = workflow_component
        self.workflow_component_output_dir: str = os.path.join(
            self.workflow_ouput_dir, workflow_component
        )

        if not os.path.isdir(self.workflow_component_output_dir):
            os.makedirs(self.workflow_component_output_dir)

        self.model_directory: str = os.path.join(
            self.workflow_component_output_dir, "model_artifacts"
        )

        self.test_files = {
            "inputs": os.path.join(self.workflow_component_output_dir, "inputs.json"),
            "inference_params": os.path.join(
                self.workflow_component_output_dir,
                "inference_params.json",
            ),
            "predictions": os.path.join(
                self.workflow_component_output_dir, "predictions.json"
            ),
        }

    @staticmethod
    def check_component_reference(workflow_component: str):
        """Check component reference."""
        if workflow_component not in WORKFLOW_COMPONENTS:
            raise ValueError(
                f"Component reference {workflow_component} must be one of the following options: "
                f"{WORKFLOW_COMPONENTS}"
            )


class IOSettings(TrackedParams):
    """Configuring container file system output locations for all 4 components."""

    # storage
    download: WorkflowComponentIOSettings = WorkflowComponentIOSettings(DOWNLOAD)
    compile: WorkflowComponentIOSettings = WorkflowComponentIOSettings(COMPILE)
    test: WorkflowComponentIOSettings = WorkflowComponentIOSettings(TEST)
    upload: WorkflowComponentIOSettings = WorkflowComponentIOSettings(UPLOAD)
    # log level
    logger_level: int = INFO

    # logging
    log_level: int = INFO

    class Config:
        env_prefix = "io_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class TokenizerSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_tokenizer for details."""

    add_special_tokens: bool = True

    class Config:
        env_prefix = "tokenizer_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class ModelTracingSettings(TrackedParams):
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

    class Config:
        env_prefix = "model_tracing_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class PipelineCompilationSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_pipeline.compile_pipeline for details."""

    pipeline_name: str
    max_length: int
    batch_size: int = 6
    neuron: bool = True
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = 1e-02
    tokenizer_settings: TokenizerSettings = TokenizerSettings()
    model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class SentPipelineCompilationSettings(PipelineCompilationSettings):
    """Sentiment pipeline compilation settings."""

    pipeline_name: str = "sent_model"
    max_length = 128

    class Config:
        env_prefix = "sent_pipeline_compilation_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompilationTestSettings(TrackedParams):
    """Compilation test settings."""

    regression_atol: float = 1e-02
    regression_rtol: float = 1e-02

    class Config:
        env_prefix = "compilation_test_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledSentTrackedModelCard(TrackedModelCard):
    """Compiled sentiment tracked model card."""

    model_type: str = "compiled"
    # --- custom fields
    # uncompiled model reference
    uncompiled_model: UncompiledTrackedModelSettings = UncompiledTrackedModelSettings()
    # model compilation params
    sent_model_compilation_settings: PipelineCompilationSettings = (
        SentPipelineCompilationSettings()
    )

    compilation_test_settings: CompilationTestSettings = CompilationTestSettings()

    class Config:
        env_prefix = "compiled_sent_tracked_model_card_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
