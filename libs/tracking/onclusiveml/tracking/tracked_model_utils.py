# Standard Library
from enum import Enum
from typing import Tuple

# 3rd party libraries
from pydantic import BaseSettings, Field, SecretStr, validator


class TrackedParams(BaseSettings):
    """Base class for all parameter classes in the tracking library. Subclassing from BaseSettings
    allows for configuring parameters via environment variables."""

    pass


class TrackedModelSpecs(TrackedParams):
    """A utility to specify the neptune ai project and model level resources.
    Also includes the parsing of the api token to help instantiate ModelVersion's..
    The `api_token` field will be excluded from the model's standard export methods."""

    # neptune ai model registry specs
    project: str = Field(..., env="neptune_project")
    model: str = Field(..., env="neptune_model_id")
    api_token: SecretStr = Field(..., env="neptune_api_token", exclude=True)


class TrackedModelTestFiles(TrackedParams):
    """A utility to specifiy the attribute paths of test files supporting regression tests, e.g
    for validating runtime environments or model compilations"""

    # neptune ai locations of test files
    inputs: str = "model/test_files/inputs"
    inference_params: str = "model/test_files/inference_params"
    predictions: str = "model/test_files/predictions"


class ModelTypes(Enum):

    base: str = "base"
    trained: str = "trained"
    compiled: str = "compiled"

    @classmethod
    def get_valid_range(cls) -> Tuple[str, str, str]:
        """Simple model type validation utility"""

        return (cls.base.value, cls.trained.value, cls.compiled.value)


class TrackedModelCard(TrackedParams):
    """A common interface for specfying model resources on neptune ai."""

    model_type: str  # 'base', 'trained' or 'compiled'; see validator below
    # the path to the model artifact attribute. passing this path to the MODEL_INITIALIZER should
    # re-create the model
    model_artifact_attribute_path: str = "model/model_artifacts"
    # the callable that returns the re-loaded model instance. Can be from custom project level
    # libraries. For example
    # ```
    # from transformers.pipelines import pipeline
    #
    # # a valid callable for a fine-tuned huggingface `sentiment-analysis` pipeline based model
    # def load_tracked_model(pipeline_dir: str):
    #   return pipeline(task='sentiment-analysis',model=pipeline_dir)
    #
    # model_loader: load_tracked_model
    # ```
    # model_loader: Callable = lambda x: x  # descoped for now
    model_test_files: TrackedModelTestFiles = (
        TrackedModelTestFiles()
    )  # class containing paths to the test file attributes

    @validator("model_type")
    def check_model_type(v: str) -> str:

        if v not in ModelTypes.get_valid_range():
            raise ValueError(
                f"Model type {v} must be one of the following valid options: "
                f"{ModelTypes.get_valid_range()}"
            )

        return v