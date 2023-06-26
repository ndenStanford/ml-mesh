# 3rd party libraries
import pytest
from locust import HttpUser

# Internal libraries
from onclusiveml.serving.rest.testing import LoadTestingParams


def test_load_testing_params_with_user_classes():

    LoadTestingParams(user_classes=[HttpUser], locustfile="")


def test_load_testing_params_with_locustfile(test_locustfile):

    LoadTestingParams(locustfile=test_locustfile)


def test_load_testing_params_raise_both_client_sources():

    with pytest.raises(ValueError):
        LoadTestingParams(user_classes=[HttpUser], locustfile="dummy_file")


def test_load_testing_params_raise_cannot_find_locustfile():

    with pytest.raises(FileNotFoundError):
        LoadTestingParams(locustfile="dummy_file")
