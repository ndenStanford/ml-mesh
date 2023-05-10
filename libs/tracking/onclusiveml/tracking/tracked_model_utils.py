# 3rd party libraries
from pydantic import BaseSettings, Field, SecretStr, validator


class TrackingParams(BaseSettings):
    """Base class for all parameter classes in the tracking library. Subclassing from BaseSettings
    allows for configuring parameters via environment variables."""

    pass


class TrackedModelSpecs(TrackingParams):
    """A utility to specify the neptune ai project and model level resources.
    Also includes the parsing of the api token to help instantiate ModelVersion's..
    The `api_token` field will be excluded from the model's standard export methods."""

    # neptune ai model registry specs
    project: str = Field(..., env="neptune_project")
    model: str = Field(..., env="neptune_model_id")
    api_token: SecretStr = Field(..., env="neptune_api_token", exclude=True)


class TrackedModelTestFiles(TrackingParams):
    """A utility to specifiy the attribute paths of test files supporting regression tests, e.g
    for validating runtime environments or model compilations"""

    # neptune ai locations of test files
    inputs: str = "model/test_files/inputs"
    inference_params: str = "model/test_files/inference_params"
    predictions: str = "model/test_files/predictions"


MODEL_TYPES = ("base", "trained", "compiled")


class TrackedModelCard(TrackingParams):
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

        if v not in MODEL_TYPES:
            raise ValueError(
                f"Model type {v} must be one of the following valid options: "
                f"{MODEL_TYPES}"
            )

        return v
