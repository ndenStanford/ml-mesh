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
    TrackedModelSpecs,
    TrackedParams,
)


# --- atomic settings and models
DOWNLOAD = "download"
COMPILE = "compile"
TEST = "test"
UPLOAD = "upload"
WORKFLOW_COMPONENTS = (DOWNLOAD, COMPILE, TEST, UPLOAD)


class UncompiledTrackedModelSpecs(TrackedModelSpecs):

    project: str = "onclusive/keywords"
    model: str = "KEYWORDS-TRAINED"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "KEYWORDS-TRAINED-1"
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)

    class Config:
        env_prefix = "uncompiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledTrackedModelSpecs(TrackedModelSpecs):

    project: str = "onclusive/keywords"
    model: str = "KEYWORDS-COMPILED"

    class Config:
        env_prefix = "compiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowOutputDir(TrackedParams):

    outpath: str = "./outputs"

    class Config:
        env_prefix = "io_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowComponentIOSettings(object):

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

        if workflow_component not in WORKFLOW_COMPONENTS:
            raise ValueError(
                f"Component reference {workflow_component} must be one of the following options: "
                f"{WORKFLOW_COMPONENTS}"
            )


class IOSettings(object):
    """Configuring container file system output locations for all 4 components"""

    # admin
    download: WorkflowComponentIOSettings = WorkflowComponentIOSettings(DOWNLOAD)
    compile: WorkflowComponentIOSettings = WorkflowComponentIOSettings(COMPILE)
    test: WorkflowComponentIOSettings = WorkflowComponentIOSettings(TEST)
    upload: WorkflowComponentIOSettings = WorkflowComponentIOSettings(UPLOAD)

    log_level: int = INFO


class TokenizerSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_tokenizer for details"""

    add_special_tokens: bool = True

    class Config:
        env_prefix = "tokenizer_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class ModelTracingSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_model.compile_model for details"""

    dynamic_batching: bool = True
    strict: bool = True
    compiler_args: List[str] = ["--fast-math", "none"]

    class Config:
        env_prefix = "model_tracing_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class PipelineCompilationSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_pipeline.compile_pipeline for details"""

    pipeline_name: str
    max_length: int
    batch_size: int = 1
    neuron: bool = False
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = 1e-02
    tokenizer_settings: TokenizerSettings = TokenizerSettings()

    if neuron:
        model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class WordPipelineCompilationSettings(PipelineCompilationSettings):

    pipeline_name: str = "word_model"
    max_length = 20

    class Config:
        env_prefix = "word_pipeline_compilation_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class DocumentPipelineCompilationSettings(PipelineCompilationSettings):

    pipeline_name = "document_model"
    max_length = 512

    class Config:
        env_prefix = "document_pipeline_compilation_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompilationTestSettings(TrackedParams):

    regression_atol: float = 1e-02
    regression_rtol: float = 1e-02

    class Config:
        env_prefix = "compilation_test_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledKeywordsTrackedModelCard(TrackedModelCard):

    model_type: str = "compiled"
    # --- custom fields
    # uncompiled model reference
    uncompiled_model: UncompiledTrackedModelSpecs = UncompiledTrackedModelSpecs()
    # model compilation params
    word_model_compilation_settings: PipelineCompilationSettings = (
        WordPipelineCompilationSettings()
    )
    document_model_compilation_settings: PipelineCompilationSettings = (
        DocumentPipelineCompilationSettings()
    )

    compilation_test_settings: CompilationTestSettings = CompilationTestSettings()

    class Config:
        env_prefix = "compiled_keywords_tracked_model_card_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
