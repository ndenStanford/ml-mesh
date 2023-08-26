"""Instrumentator tests."""

# 3rd party libraries
import pytest
from prometheus_client import REGISTRY
from prometheus_client.metrics_core import Metric
from starlette.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.observability.metrics import REGISTERED_METRICS
from onclusiveml.serving.rest.observability.utils import get_full_name


class NotTrackedMetricError(Exception):
    pass


def assert_metric_value(
    expected: float = 0.0,
    metric: Metric = None,
    app_name: str = "test",
    path: str = "/metrics",
    method: str = "GET",
    status_code: str = "200",
    exception_type: str = "AttributeError",
) -> None:
    """A utility function that asserts that the metric value for the
       given parameters in the Prometheus metrics registry matches the
       expected value.

    Args:
        expected (float): The expected count of requests that should be recorded
                          in the metrics.
        metric (Metric, optional): The metric to check.
        app_name (str, optional): The name of the application to filter the metric by.
        path (str, optional): The endpoint path to filter the metric by.
        method (str, optional): The HTTP method to filter the metric by.
        status_code (str, optional): The HTTP status code to filter the metric by.
        exception_type (str, optional): The Exception type.
    Raises:
        NotTrackedMetricError: Unknown Metric
    """
    params = []
    full_metric_name = get_full_name(metric)
    if full_metric_name == "fastapi_responses_total":
        params = [
            full_metric_name,
            {
                "app_name": app_name,
                "path": path,
                "method": method,
                "status_code": status_code,
            },
        ]
    elif full_metric_name == "fastapi_app_info":
        params = [full_metric_name, {"app_name": app_name}]
    elif full_metric_name in (
        "fastapi_requests_total",
        "fastapi_requests_duration_seconds",
        "fastapi_requests_in_progress",
    ):
        params = [
            full_metric_name,
            {"app_name": app_name, "path": path, "method": method},
        ]
    elif full_metric_name == "fastapi_exceptions_total":
        params = [
            full_metric_name,
            {
                "app_name": app_name,
                "path": path,
                "method": method,
                "exception_type": exception_type,
            },
        ]
    else:
        raise NotTrackedMetricError(f"Not tracked metric: {metric}")

    result = REGISTRY.get_sample_value(*params)
    result = result or 0.0

    assert result == expected
    assert result + 1.0 != expected


def test_metrics_endpoint(test_model_server):
    """Tests initialization of the Instrumentator with ModelServer."""
    metrics_endpoint = (
        Instrumentator(test_model_server, app_name="test").setup().metrics_endpoint
    )

    test_metrics_routes = [
        route.path
        for route in test_model_server.router.routes
        if route.path.startswith(f"{metrics_endpoint}")
    ]
    assert test_metrics_routes == [metrics_endpoint]


@pytest.mark.parametrize(
    "url, expected_app_info, expected_total, expected_rest",
    [
        ("/v1/live", 1.0, 1.0, 0.0),
        ("/v1/ready", 2.0, 1.0, 0.0),
        ("/v1/live", 3.0, 2.0, 0.0),
        ("/v1/ready", 4.0, 2.0, 0.0),
    ],
)
def test_metrics_values(
    test_model_server, url, expected_app_info, expected_total, expected_rest
):
    """Tests if the metrics endpoint returns the expected response."""
    metrics_endpoint = (
        Instrumentator(test_model_server, app_name="test").setup().metrics_endpoint
    )
    client = TestClient(test_model_server)
    response = client.get(url)
    assert response.status_code == 200
    response = client.get(metrics_endpoint)
    assert response.status_code == 200

    for test_metric in REGISTERED_METRICS:
        full_name = get_full_name(test_metric)
        if full_name in ("fastapi_app_info"):
            assert_metric_value(expected_app_info, test_metric, path=url)
        elif full_name in (
            "fastapi_responses_total",
            "fastapi_requests_total",
        ):
            assert_metric_value(expected_total, test_metric, path=url)
        elif full_name in (
            "fastapi_exceptions_total",
            "fastapi_requests_in_progress",
            "fastapi_requests_duration_seconds",
        ):
            assert_metric_value(expected_rest, test_metric, path=url)
        else:
            raise NotTrackedMetricError(f"Not tracked metric: {test_metric}")
