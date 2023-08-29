"""Load test parameters test."""

# 3rd party libraries
import pytest
from locust import HttpUser

# Internal libraries
from libs.serving.onclusiveml.serving.rest.testing.load_test import (
    LoadTestingParams,
)


def test_load_testing_params_with_user_classes():
    """Tests the initialization of the LoadTestingParams class using the user_classes arg."""
    LoadTestingParams(user_classes=[HttpUser], locustfile="")


def test_load_testing_params_with_locustfile(test_locustfile):
    """Tests the initialization of the LoadTestingParams class using the locustfile arg.."""
    LoadTestingParams(locustfile=test_locustfile)


def test_load_testing_params_raise_both_client_sources():
    """Tests the error behaviour of initializing a LoadTestingParams instance."""
    with pytest.raises(ValueError):
        LoadTestingParams(user_classes=[HttpUser], locustfile="dummy_file")


def test_load_testing_params_raise_cannot_find_locustfile():
    """Failed initialition of a LoadTestingParams instance."""
    with pytest.raises(FileNotFoundError):
        LoadTestingParams(locustfile="dummy_file")
