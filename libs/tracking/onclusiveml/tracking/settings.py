"""Tracking settings."""

# Standard Library
from typing import Optional

# 3rd party libraries
from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings, OnclusiveSecretStr
from onclusiveml.core.constants import Environment
from onclusiveml.tracking.constants import ModelType


class TrackingSettings(OnclusiveBaseSettings):
    """Base class for all parameter classes in the tracking library.

    Subclassing from BaseSettings allows for configuring parameters via environment variables.
    """


class TrackingBackendSettings(TrackingSettings):
    """Entrypoint to configure the tracking library's S3 storage backend behaviour \
    via environment variables.

    The values derived by this class's attributes will be used as default values for the
    identically named TrackedModelVersion class' constructor arguments:
        - use_s3_backend
        - environment
        - s3_bucket_prefix
        - s3_backend_root
    """

    environment: Environment
    use_s3_backend: bool = True
    s3_bucket_prefix: str = "onclusive-model-store-"
    s3_backend_root: str = "neptune-ai-model-registry"

    model_config = SettingsConfigDict(env_prefix="onclusiveml_tracking_backend_")

    @property
    def bucket_name(self) -> str:
        """S3 bucket name."""
        return f"{self.s3_bucket_prefix}{self.environment}"


class TrackedGithubActionsSpecs(OnclusiveBaseSettings):
    """A class used for capturing the most relevent Github Actions build environment variables.

    Generate a CI lineage for any process being executed by Github Actions workflows, e.g. model
    compilation.

    For details on the definitions of these and all other variables available, see
    https://docs.github.com/en/actions/learn-github-actions/variables
    """

    github_repository: str = "github_repository"
    github_actor: str = "github_actor"
    github_env: str = "github_env"
    github_workflow: str = "github_workflow"
    github_job: str = "github_job"
    github_ref: str = "github_ref"
    github_base_ref: str = "github_base_ref"
    github_head_ref: str = "github_head_ref"
    github_sha: str = "github_sha"
    github_event_name: str = "github_event_name"
    github_run_id: str = "github_run_id"
    github_run_number: str = "github_run_number"
    runner_arch: str = "runner_arch"
    runner_name: str = "runner_name"
    runner_os: str = "runner_os"


class TrackedImageSpecs(OnclusiveBaseSettings):
    """A class to capture the specs of a given docker image."""

    docker_image_name: str = "image_name"
    docker_image_tag: str = "image_tag"


class TrackedModelSettings(OnclusiveBaseSettings):
    """A utility to specify the neptune ai project and model level resources.

    Also includes the parsing of the api token to help instantiate ModelVersion's..
    The `api_token` field will be excluded from the model's standard export methods.
    """

    # neptune ai model registry specs
    project: str
    model: str
    api_token: Optional[OnclusiveSecretStr] = Field(default=None, exclude=True)
    with_id: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="onclusiveml_neptune_")


class TrackedModelTestFiles(TrackingSettings):
    """A utility to specifiy the attribute paths of test files supporting regression tests."""

    # neptune ai locations of test files
    inputs: str = "model/test_files/inputs"
    inference_params: str = "model/test_files/inference_params"
    predictions: str = "model/test_files/predictions"


class TrackedModelCard(TrackingSettings):
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
    # the path to the dataset used in model training
    training_data_attribute_path: str = "data/train"

    @field_validator("model_type")
    def check_model_type(v: str) -> str:
        """Check model type."""
        if v not in ModelType.values():
            raise ValueError(
                f"Model type {v} must be one of the following valid options: "
                f"{ModelType.values()}"
            )

        return v

    github_action_context: TrackedGithubActionsSpecs = TrackedGithubActionsSpecs()

    model_config = SettingsConfigDict(protected_namespaces=("settings_",))
