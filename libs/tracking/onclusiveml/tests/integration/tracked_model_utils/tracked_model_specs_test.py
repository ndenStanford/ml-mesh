"""Tracked model specs tests."""

# Standard Library
import os

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import TrackedModelSpecs


def test_from_env():
    """Tests getting data from environment variables.

    Note:
        This test relies on the following environment variables being set.
            - NEPTUNE_PROJECT
            - NEPTUNE_MODEL_ID
            - NEPTUNE_API_TOKEN
    """
    tracked_model_specs = TrackedModelSpecs()

    assert tracked_model_specs.project == os.environ["NEPTUNE_PROJECT"]
    assert tracked_model_specs.model == os.environ["NEPTUNE_MODEL_ID"]
    # api token needs to be accessed via the SecretString's  `_secret_value` field attribute
    assert (
        tracked_model_specs.api_token._secret_value == os.environ["NEPTUNE_API_TOKEN"]
    )
