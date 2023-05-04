# Standard Library
import os
from typing import List

# 3rd party libraries
from pydantic import BaseSettings, validator

# Internal libraries
from onclusiveml.tracking import TrackedModelCard, TrackedModelSpecs


# --- atomic settings and models
DOWNLOAD = "download"
COMPILE = "compile"
VALIDATE = "validate"
UPLOAD = "upload"
WORKFLOW_COMPONENTS = (DOWNLOAD, COMPILE, VALIDATE, UPLOAD)


class UncompiledTrackedModelSpecs(TrackedModelSpecs):

    project: str = "onclusive/keywords"
    model: str = "KEYWORDS-BASE"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "KEYWORDS-BASE-6"


class CompiledTrackedModelSpecs(TrackedModelSpecs):

    project: str = "onclusive/keywords"
    model: str = "KEYWORDS-COMPILED"


class OutputDirectory(BaseSettings):

    parent_directory: str = "./outputs"
    compilation_workflow_component: str = "download"

    model_directory = os.path.join(
        parent_directory, compilation_workflow_component, "model_artifacts"
    )
    inputs = os.path.join(
        parent_directory, compilation_workflow_component, "test_files", "inputs"
    )
    inference_params = os.path.join(
        parent_directory,
        compilation_workflow_component,
        "test_files",
        "inference_params",
    )
    predictions = os.path.join(
        parent_directory, compilation_workflow_component, "test_files", "predictions"
    )

    @validator("compilation_workflow_component")
    def check_component_reference(v):

        if v not in WORKFLOW_COMPONENTS:
            raise ValueError(
                f"Component reference {v} must be one of the following options: "
                f"{WORKFLOW_COMPONENTS}"
            )


class TokenizerSettings(BaseSettings):
    """See libs.compile.onclusiveml.compile.compiled_tokenizer for details"""

    add_special_tokens: bool = True


class ModelTracingSettings(BaseSettings):
    """See libs.compile.onclusiveml.compile.compiled_model.compile_model for details"""

    dynamic_batching: bool = True
    strict: bool = True
    compiler_args: List[str] = ["--fast-math", "none"]


class PipelineCompilationSettings(BaseSettings):
    """See libs.compile.onclusiveml.compile.compiled_pipeline.compile_pipeline for details"""

    pipeline_name: str
    max_length: int
    batch_size: int
    neuron: bool = True
    validate_compilation: bool = True
    validation_rtol: float = 1e-02
    validation_atol: float = (1e-02,)
    tokenizer_settings: TokenizerSettings = TokenizerSettings()
    model_tracing_settings: ModelTracingSettings = ModelTracingSettings()


class WordEmbeddingCompilationSettings(PipelineCompilationSettings):

    pipeline_name: str = "word_model"
    max_length = 20

    class Config:
        env_prefix = "word_model_"


class PipelineEmbeddingCompilationSettings(PipelineCompilationSettings):

    pipeline_name = "document_model"
    max_length = 512

    class Config:
        env_prefix = "document_model_"


class TrackedKeywordsCompiledModelCard(TrackedModelCard):

    model_type: str = "compiled"
    # --- custom fields
    # model compilation params
    word_model_compilation_settings: WordEmbeddingCompilationSettings = (
        WordEmbeddingCompilationSettings()
    )
    document_model_compilation_settings: PipelineEmbeddingCompilationSettings = (
        PipelineEmbeddingCompilationSettings()
    )
    # validation params
    regression_atol: float = 1e-02
    regression_rtol: float = 1e-02


# ---component level settings and models
class UncompiledKeywordModelDownloadSettings(BaseSettings):
    """Settings for module/component `download_uncompiled_model.py`"""

    # uncompiled model specs
    tracked_model_specs: TrackedModelSpecs = UncompiledTrackedModelSpecs()
    # admin
    local_output_dir = OutputDirectory(parent_directory="download")
    logging_level: str = "INFO"
    # prefix environment variable counterparts of all above fields

    class Config:

        env_prefix = "download_"


class CompileKeywordsModelSettings(BaseSettings):
    """Settings for module/component `compile_model.py`"""

    # admin
    local_output_dir = OutputDirectory(parent_directory="compile")
    logging_level: str = "INFO"
    # prefix environment variable counterparts of all above fields

    class Config:

        env_prefix = "compiled_"


class ValidateCompiledKeywordsModelSettings(BaseSettings):
    """Settings for module/component `validate_compiled_model.py`"""

    # admin
    local_output_dir = OutputDirectory(parent_directory="validate")
    logging_level: str = "INFO"
    # prefix environment variable counterparts of all above fields

    class Config:

        env_prefix = "validate_"


class UploadValidatedCompiledKeywordModelSettings(BaseSettings):
    """Settings for module/component `upload_compiled_model.py`"""

    # compiled model specs
    compiled_model_specs: TrackedModelSpecs = CompiledTrackedModelSpecs()

    # prefix environment variable counterparts of all above fields

    class Config:

        env_prefix = "upload_"
