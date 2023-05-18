# Standard Library
import os

# 3rd party libraries
import pytest
from pydantic import ValidationError

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import TrackedModelSpecs


@pytest.mark.parametrize(
    "project,model,api_token",
    [("a", "b", "c"), ("some project", "some model", "some token")],
)
def test_from_env(project, model, api_token):

    for env_name, env_val in (
        ("neptune_project", project),
        ("neptune_model_id", model),
        ("NEPTUNE_API_TOKEN", api_token),  # tests case insensitivity
    ):
        os.environ[env_name] = env_val

    tracked_model_specs = TrackedModelSpecs()

    assert tracked_model_specs.project == project
    assert tracked_model_specs.model == model
    # api token needs to be accessed via the SecretString's  `_secret_value` field attribute
    assert tracked_model_specs.api_token._secret_value == api_token
    # clean up env var namespace
    for env_name, env_val in (
        ("neptune_project", project),
        ("neptune_model_id", model),
        ("NEPTUNE_API_TOKEN", api_token),
    ):
        del os.environ[env_name]


def test_from_empty_env_raise_error():

    with pytest.raises(ValidationError):
        TrackedModelSpecs()


def test_to_dict_raise():

    test_specs = TrackedModelSpecs(project="a", model="b", api_token="secret_token")
    test_specs_dict = test_specs.dict()

    test_specs_dict["project"], test_specs_dict["model"]

    with pytest.raises(KeyError):
        test_specs_dict["api_token"]
