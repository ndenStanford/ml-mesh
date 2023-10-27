"""Model server tests."""
# Standard Library

# 3rd party libraries
import pytest
import requests

# Internal libraries
from libs.serving.onclusiveml.tests.functional.conftest import (
    RootResponse,
    TestBioResponseModel,
    TestModelPredictRequestModel,
    TestModelPredictResponseModel,
    TestPrediction,
    TestRecord,
)
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)
from onclusiveml.serving.rest.serve.server_utils import get_model_server_urls


# import pdb
# pdb.set_trace()


# --- server
@pytest.mark.order(1)
@pytest.mark.server
def test_model_server_serve_with_model(test_model_server):
    """Test model server serve method with model.

    Launches a fully fledged ModelServer hosting all utility endpoints as well as a loaded
    instance of the TestServedModel model class, and keeps it running until stopped manually.

    Designed for manual testing during development, not for CI due to library test suite setup
    limitations.
    """
    test_model_server.serve()


# --- client - root, liveness, readiness
@pytest.mark.order(2)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_url_reference, test_probe_response_model",
    [
        ("root", RootResponse),
        ("liveness", LivenessProbeResponse),
        ("readiness", ReadinessProbeResponse),
    ],
)
def test_model_server_client_no_model(
    test_api_version,
    test_model_name,
    test_port,
    test_url_reference,
    test_probe_response_model,
):
    """Tests the availability and response format of a live ModelServer endpoints.

    Endpoints:
        - root,
        - liveness,
        -readiness
    as launched by the test_model_server_serve_with_model test case.

    Requires test_model_server_serve_with_model to have been called on the same machine
    """
    test_model_server_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    url = f"http://localhost:{test_port}" + getattr(
        test_model_server_urls, test_url_reference
    )

    response = requests.get(url)

    print(response)

    test_probe_response_model(**response.json())


# --- client - model predict
@pytest.mark.order(4)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_request_data, test_response_model, test_response_expected",
    [
        (
            TestModelPredictRequestModel(
                instances=[
                    TestRecord(number_of_legs=0),
                ]
            ),
            TestModelPredictResponseModel,
            TestModelPredictResponseModel(
                predictions=[
                    TestPrediction(animal="snake"),
                ]
            ),
        ),
        (
            TestModelPredictRequestModel(
                instances=[
                    TestRecord(number_of_legs=1),
                    TestRecord(number_of_legs=2),
                    TestRecord(number_of_legs=4),
                    TestRecord(number_of_legs=10),
                ]
            ),
            TestModelPredictResponseModel,
            TestModelPredictResponseModel(
                predictions=[
                    TestPrediction(animal="flamingo"),
                    TestPrediction(animal="robin"),
                    TestPrediction(animal="dog"),
                    TestPrediction(animal="dog"),
                ]
            ),
        ),
    ],
)
def test_model_server_serve_predict(
    test_api_version,
    test_port,
    test_model_name,
    test_request_data,
    test_response_model,
    test_response_expected,
):
    """Tests the availability and response format of a live ModelServer's model predict endpoint.

    Requires test_model_server_serve_with_model to have been called on the same machine.
    """
    test_model_server_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    model_predict_url = (
        f"http://localhost:{test_port}" + test_model_server_urls.model_predict
    )

    response = requests.post(model_predict_url, json=test_request_data.dict())

    test_response_actual = test_response_model(**response.json())

    assert test_response_actual == test_response_expected


# --- client - model bio
@pytest.mark.order(3)
@pytest.mark.client
@pytest.mark.parametrize(
    "test_response_model",
    [TestBioResponseModel],
)
def test_model_server_serve_bio(
    test_api_version,
    test_port,
    test_model_name,
    test_response_model,
):
    """Tests the availability and response format of a live ModelServer's model bio endpoint."""
    test_model_server_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    model_bio_url = f"http://localhost:{test_port}" + test_model_server_urls.model_bio

    response = requests.get(model_bio_url)

    test_response_actual = test_response_model(**response.json())
    test_response_expected = TestBioResponseModel(name=test_model_name)

    assert test_response_actual == test_response_expected
