# Standard Library
import os
import sys
import time

# 3rd party libraries
import pytest
from prometheus_client import REGISTRY
from starlette.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ServedModel
from onclusiveml.serving.rest.serve.server_utils import get_model_server_urls


# import TestServedModel in serve directory
current_dir = os.path.dirname(os.path.abspath(__file__))
rest_dir = os.path.dirname(current_dir)
serve_dir = os.path.join(rest_dir, "serve")
sys.path.insert(0, serve_dir)

# 3rd party libraries
from served_model_test import TestServedModel


def assert_request_count(
    expected: float,
    name: str = "fastapi_responses_total",
    app_name: str = "test",
    path: str = "/metrics",
    method: str = "GET",
    status_code: str = "200",
) -> None:
    """
    A utility function that asserts that the request count for the given parameters
    in the Prometheus metrics registry matches the expected value.

    Args:
        expected (float): The expected count of requests that should be recorded
                          in the metrics.
        name (str, optional): The name of the metric to check.
        app_name (str, optional): The name of the application to filter the metric by.
        path (str, optional): The endpoint path to filter the metric by.
        method (str, optional): The HTTP method to filter the metric by.
        status_code (str, optional): The HTTP status code to filter the metric by.

    Raises:
        AssertionError: If the retrieved count from the Prometheus registry does not match
                        the expected value, or if incrementing the retrieved count by 1
                        still equals the expected value.
    """
    result = REGISTRY.get_sample_value(
        name,
        {
            "app_name": app_name,
            "path": path,
            "method": method,
            "status_code": status_code,
        },
    )
    assert result == expected
    assert result + 1.0 != expected


@pytest.mark.parametrize("test_served_model_class", [ServedModel, TestServedModel])
@pytest.mark.parametrize(
    "test_add_model_predict, test_add_model_bio, test_api_version, test_on_startup",
    [
        (False, False, "v1", lambda x: time.time(1)),
        (False, True, "v2", []),
        (True, True, "v3", lambda x: time.time(1)),
        (True, False, "v4", []),
    ],
)
def test_model_server___init__with_model(setup_model_server):
    """Tests initialization of the Instrumentator with ModelServer
    - tests metrics endpoint is exposed
    """
    test_model_server = setup_model_server
    metrics_endpoint = (
        Instrumentator(test_model_server, app_name="test").setup().metrics_endpoint
    )

    test_metrics_routes = [
        route.path
        for route in test_model_server.router.routes
        if route.path.startswith(f"{metrics_endpoint}")
    ]
    assert test_metrics_routes == [metrics_endpoint]


@pytest.mark.parametrize("test_served_model_class", [TestServedModel])
@pytest.mark.parametrize(
    "test_add_model_predict, test_add_model_bio, test_api_version, test_on_startup",
    [
        (False, False, "v1", lambda x: time.time(1)),
        (False, True, "v2", []),
        (True, True, "v3", lambda x: time.time(1)),
        (True, False, "v4", []),
    ],
)
def test_expose_return_prometheus_metrics(setup_model_server):
    """Tests if the metrics endpoint returns the expected response"""

    test_model_server = setup_model_server
    metrics_endpoint = (
        Instrumentator(test_model_server, app_name="test").setup().metrics_endpoint
    )
    client = TestClient(test_model_server)

    response = client.get(metrics_endpoint)
    assert response.status_code == 200
    assert 'fastapi_app_info{app_name="test"}' in response.text


@pytest.mark.parametrize("test_served_model_class", [TestServedModel])
@pytest.mark.parametrize(
    "test_add_model_predict, test_add_model_bio, test_api_version, test_on_startup",
    [
        (True, True, "v1", lambda x: time.time(1)),
    ],
)
def test_metrics_request_count(setup_model_server):
    """Tests if the metrics endpoint returns the expected response"""

    test_model_server = setup_model_server
    metrics_endpoint = (
        Instrumentator(test_model_server, app_name="test").setup().metrics_endpoint
    )
    client = TestClient(test_model_server)
    liveness_url = get_model_server_urls(api_version="v1").liveness
    response = client.get(liveness_url)
    assert response.status_code == 200
    response = client.get(metrics_endpoint)
    assert_request_count(1, path=liveness_url)

    response = client.get(liveness_url)
    assert response.status_code == 200
    response = client.get(metrics_endpoint)
    assert_request_count(2, path=liveness_url)

    response = client.get(liveness_url)
    assert response.status_code == 200
    response = client.get(metrics_endpoint)
    assert_request_count(3, path=liveness_url)
