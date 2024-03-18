"""Settings."""

# 3rd party libraries
from neptune.types.mode import Mode
from pydantic import Field

# Internal libraries
from onclusiveml.tracking import TrackedModelSpecs, TrackedParams


class UncompiledTrackedModelSpecs(TrackedModelSpecs):
    """Tracked specifications for an uncompiled model.

    Attributes:
        project (str): The project name for the model.
        model (str): Model name
        with_id (str): Unique identifier for the model version
        model (str): Mode of interaction with the model
    """

    project: str = "onclusive/content-scoring"
    model: str = "CONTENT-SCORING-TRAINED"
    # we need an additional version tag since we are referencing an EXISTING model version, rather
    # than creating a new one
    with_id: str = "CONTENT-SCORING-TRAINED-1"
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
        input_dir (str): Directory path for input data
        output_dir (str): Directory path for output data
        target_format (str): The format of the target data
    """

    project: str = "onclusive/content-scoring"
    model: str = "CONTENT-SCORING-COMPILED"
    input_dir: str = "projects/content-scoring/train/data/model.joblib"
    output_dir: str = "data/model.pt"
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
