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
    """Tracked specifications for an uncompiled model.

    Attributes:
        project (str): The project name for the model.
        model (str): Model name
        with_id (str): Unique identifier for the model version
        model (str): Mode of interaction with the model
    """

    project: str = "onclusive/ner"
    model: str = "NER-TRAINED"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "NER-TRAINED-41"
    # we only need to download from the base model, not upload
    mode: str = Field(Mode.READ_ONLY)

    class Config:
        env_prefix = "uncompiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledTrackedModelSpecs(TrackedModelSpecs):
    """Tracked specifications for a compiled model.

    Attributes:
        project (str): The project name for the model
        model (str): The model name
    """

    project: str = "onclusive/ner"
    model: str = "NER-COMPILED"

    class Config:
        env_prefix = "compiled_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowOutputDir(TrackedParams):
    """Parameters for the output directory.

    Attributes:
        outpath (str): The output directory path
    """

    outpath: str = "./outputs"

    class Config:
        env_prefix = "io_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class WorkflowComponentIOSettings(object):
    """I/O settings for a workflow component.

    Attributes:
        workflow_ouput_dir (str): Base output directory
        workflow_component (str): Name of workflow component
        workflow_component_output_dir (str): The output directory specific to the component
        model_directory (str): The directory for model artifacts
        model_directory_base (str): The directory for base NER model
        model_directory_kj (str): The directory for NER model used for korean/japanese
        test_files (dict): Paths to test related files

    """

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

        self.model_directory_base: str = os.path.join(
            self.workflow_component_output_dir, "model_artifacts/base_ner"
        )
        self.model_directory_kj: str = os.path.join(
            self.workflow_component_output_dir, "model_artifacts/korean_japanese_ner"
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


class IOSettings(object):
    """Configuring container file system output locations for all 4 components.

    Attributes:
        download (WorkflowComponentIOSettings): I/O settings for download component
        compile (WorkflowComponentIOSettings): I/O settings for compile component
        test (WorkflowComponentIOSettings): I/O settings for test component
        upload (WorkflowComponentIOSettings): I/O settings for upload component

    """

    # admin
    download: WorkflowComponentIOSettings = WorkflowComponentIOSettings(DOWNLOAD)
    compile: WorkflowComponentIOSettings = WorkflowComponentIOSettings(COMPILE)
    test: WorkflowComponentIOSettings = WorkflowComponentIOSettings(TEST)
    upload: WorkflowComponentIOSettings = WorkflowComponentIOSettings(UPLOAD)

    log_level: int = INFO


class TokenizerSettings(TrackedParams):
    """See libs.compile.onclusiveml.compile.compiled_tokenizer for details.

    Attributes:
        add_special_tokens (bool): Flag for adding special tokens
    """

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
    strict: bool = True
    compiler_args: List[str] = ["--fast-math", "none"]

    class Config:
        env_prefix = "model_tracing_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class PipelineCompilationSettings(TrackedParams):
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
    batch_size: int = 6
    neuron: bool = False
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = 1e-02
    tokenizer_settings: TokenizerSettings = TokenizerSettings()
    model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class NERPipelineCompilationSettings(PipelineCompilationSettings):
    """Tracked model card for a compiled NER model.

    Attributes:
        pipeline_name (str): Name of the NER pipeline
        max_length (int): Max sequence length for NER
    """

    pipeline_name: str = "ner_model"
    max_length = 128

    class Config:
        env_prefix = "ner_pipeline_compilation_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompilationTestSettings(TrackedParams):
    """Settings for compilation tests.

    Attributes:
        regression_atol (float): Relative tolerance for validation
        regression_rtol (float): Absolute tolerance for validation
    """

    regression_atol: float = 1e-02
    regression_rtol: float = 1e-02

    class Config:
        env_prefix = "compilation_test_settings_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"


class CompiledNERTrackedModelCard(TrackedModelCard):
    """Tracked model card for a compiled NER model.

    Attributes:
        model_type(str): Type of the model card
        uncompiled_model (UncompiledTrackedModelSpecs): Specifications for the uncompiled model
        ner_model_compilation_settings (PipelineCompilationSettings): Compilation settings
        compilation_test_settings (CompilationTestSettings): Compilation test settings
    """

    model_type: str = "compiled"
    # --- custom fields
    # uncompiled model reference
    uncompiled_model: UncompiledTrackedModelSpecs = UncompiledTrackedModelSpecs()
    # model compilation params
    ner_model_compilation_settings: PipelineCompilationSettings = (
        NERPipelineCompilationSettings()
    )

    compilation_test_settings: CompilationTestSettings = CompilationTestSettings()

    class Config:
        env_prefix = "compiled_ner_tracked_model_card_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
