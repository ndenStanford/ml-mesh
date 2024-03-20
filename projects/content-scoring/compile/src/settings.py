"""Settings."""

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import TrackedModelSpecs, TrackedParams


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

    project: str = "onclusive/document-content-scoring"
    model: str = "DOCUMENT-SCORING"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "DOCUMENT-SCORING-18"
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

    project: str = "onclusive/document-content-scoring"
    model: str = "DOCUMENT-COMPILED"
    target_format: str = "torch"

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
        env_prefix = "compiled_pipeline_io_"
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

    @staticmethod
    def check_component_reference(workflow_component: str):
        """Check component reference."""
        if workflow_component not in WORKFLOW_COMPONENTS:
            raise ValueError(
                f"Component reference {workflow_component} must be one of the following options: "
                f"{WORKFLOW_COMPONENTS}"
            )


class IOSettings(TrackedParams):
    """Configuring container file system output locations for all 4 components.

    Attributes:
        download (WorkflowComponentIOSettings): I/O settings for download component
        compile (WorkflowComponentIOSettings): I/O settings for compile component
        test (WorkflowComponentIOSettings): I/O settings for test component
        upload (WorkflowComponentIOSettings): I/O settings for upload component

    """

    # storage
    download: WorkflowComponentIOSettings = WorkflowComponentIOSettings(DOWNLOAD)
    compile: WorkflowComponentIOSettings = WorkflowComponentIOSettings(COMPILE)
    test: WorkflowComponentIOSettings = WorkflowComponentIOSettings(TEST)
    upload: WorkflowComponentIOSettings = WorkflowComponentIOSettings(UPLOAD)
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
    batch_size: int = 1
    neuron: bool = True
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = 1e-02
    tokenizer_settings: TokenizerSettings = TokenizerSettings()
    model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class CompiledContentScoringTrackedModelCard(TrackedModelCard):
    """Compiled iptc tracked model card."""

    model_type: str = "compiled"

    uncompiled_model: UncompiledTrackedModelSpecs = UncompiledTrackedModelSpecs()

    class Config:
        env_prefix = "compiled_iptc_tracked_model_card_"
        env_file = "config/dev.env"
        env_file_encoding = "utf-8"
