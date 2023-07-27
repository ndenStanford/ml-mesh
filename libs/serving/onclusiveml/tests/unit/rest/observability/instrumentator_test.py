# Standard Library
import os
import sys
import time

# 3rd party libraries
import pytest
from starlette.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ServedModel


# import TestServedModel in serve directory
current_dir = os.path.dirname(os.path.abspath(__file__))
rest_dir = os.path.dirname(current_dir)
serve_dir = os.path.join(rest_dir, "serve")
sys.path.insert(0, serve_dir)

# 3rd party libraries
from served_model_test import TestServedModel


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
def test_expose_return_prometheus_metrics(setup_model_server):
    """Tests if the metrics endpoint returns the expected response"""

    test_model_server = setup_model_server
    Instrumentator.enable(test_model_server, app_name="test")
    client = TestClient(test_model_server)

    response = client.get("/metrics")
    assert response.status_code == 200
    assert 'fastapi_app_info{app_name="test"}' in response.text
