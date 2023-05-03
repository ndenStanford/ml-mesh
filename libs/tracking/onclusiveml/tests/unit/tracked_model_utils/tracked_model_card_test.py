# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import (
    TrackedModelCard,
    TrackedModelSpecs,
    TrackedModelTestFiles,
)


@pytest.mark.parametrize(
    "project,model,api_token,inputs,inference_params,predictions,"
    "model_type,model_artifact_attribute_path",
    [
        (
            "project",
            "model",
            "token",
            "inputs",
            "inference_params",
            "predictions",
            "base",
            "artifacts",
        ),
        (
            "project",
            "model",
            "token",
            "inputs",
            "inference_params",
            "predictions",
            "trained",
            "artifacts",
        ),
        (
            "project",
            "model",
            "token",
            "inputs",
            "inference_params",
            "predictions",
            "compiled",
            "artifacts",
        ),
    ],
)
def from_env_test(
    project,
    model,
    api_token,
    inputs,
    inference_params,
    predictions,
    model_type,
    model_artifact_attribute_path,
    # model_loader,
):
    # set env vars
    for env_name, env_val in (
        # specs
        ("neptune_project", project),
        ("neptune_model_id", model),
        ("NEPTUNE_API_TOKEN", api_token),  # tests case insensitivity
        # test files
        ("inputs", inputs),
        ("inference_params", inference_params),
        ("predictions", predictions),
        # model card
        ("model_type", model_type),
        ("model_artifact_attribute_path", model_artifact_attribute_path),
    ):
        os.environ[env_name] = env_val
    # create model card
    tracked_model_specs = TrackedModelSpecs()
    tracked_model_test_files = TrackedModelTestFiles()
    tracked_model_card = TrackedModelCard(
        model_specs=tracked_model_specs,
        model_test_files=tracked_model_test_files,
        # model_loader=model_loader,
    )
    # TrackedModelCard attributes
    assert (
        tracked_model_card.model_artifact_attribute_path
        == model_artifact_attribute_path
    )
    assert tracked_model_card.model_type == model_type

    # clean up env var namespace
    for env_name, env_val in (
        # specs
        ("neptune_project", project),
        ("neptune_model_id", model),
        ("NEPTUNE_API_TOKEN", api_token),
        # test files
        ("inputs", inputs),
        ("inference_params", inference_params),
        ("predictions", predictions),
        # model card
        ("model_type", model_type),
        ("model_artifact_attribute_path", model_artifact_attribute_path),
    ):
        del os.environ[env_name]
