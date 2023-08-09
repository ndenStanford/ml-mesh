# Standard Library
from unittest.mock import Mock, patch

# 3rd party libraries
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from served_model_test import TestServedModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    ServedModel,
    get_liveness_router,
    get_model_bio_router,
    get_model_predict_router,
    get_readiness_router,
    get_root_router,
)
from onclusiveml.serving.rest.serve.server_models import ServedModelMethods
from onclusiveml.serving.rest.serve.server_utils import get_model_server_urls


@pytest.mark.parametrize(
    "test_kwargs,root_url_expected,liveness_url_expected,readiness_url_expected,predict_url_expected,bio_url_expected",  # noqa: E501
    [
        (
            {},  # test defaults
            "/",
            "/live",
            "/ready",
            "/model/no_model/predict",
            "/model/no_model/bio",
        ),
        (
            {"api_version": "test-version", "model_name": "test-model"},
            "/test-version/",
            "/test-version/live",
            "/test-version/ready",
            "/test-version/model/test-model/predict",
            "/test-version/model/test-model/bio",
        ),
    ],
)
def test_get_model_server_urls(
    test_kwargs,
    root_url_expected,
    liveness_url_expected,
    readiness_url_expected,
    predict_url_expected,
    bio_url_expected,
):
    """Tests the utility method get_model_server_urls to produce correctly parametrized urls
    - with & without specified api version
    - with & without a model"""

    test_urls = get_model_server_urls(**test_kwargs)

    assert test_urls.root == root_url_expected
    assert test_urls.liveness == liveness_url_expected
    assert test_urls.readiness == readiness_url_expected
    assert test_urls.model_predict == predict_url_expected
    assert test_urls.model_bio == bio_url_expected


@pytest.fixture
def mocked_requests(mocker):
    return mocker.patch("onclusiveml.serving.rest.serve.server_utils.requests")


def test_liveness_router_with_betterstack_settings(mocked_requests):
    """Test liveness router with BetterStack settings"""
    # Mock the betterstack_settings environment and betterstack_key
    with patch(
        "onclusiveml.serving.rest.serve.server_utils.get_betterstack_settings"
    ) as mock_get_betterstack_settings:
        mock_betterstack_settings = Mock()
        mock_betterstack_settings.environment = "prod"
        mock_betterstack_settings.betterstack_key = "test-key"
        mock_get_betterstack_settings.return_value = mock_betterstack_settings
        # Create a test client and call the liveness endpoint
        app = FastAPI()

        test_client = TestClient(app)
        response = test_client.get("/live")
        # Assertions
        assert response.status_code == 200
        assert response.json() == {"status": "alive"}
        # Verify that the request to BetterStack API was made
        mocked_requests.post.assert_called_once_with(
            "https://uptime.betterstack.com/api/v1/heartbeat/test-key"
        )


@pytest.mark.parametrize(
    "get_router_method, test_api_version, test_route_url_expected",
    [
        (get_root_router, "v2", get_model_server_urls(api_version="v2").root),
        (get_root_router, "test", get_model_server_urls(api_version="test").root),
        (
            get_liveness_router,
            "v2",
            get_model_server_urls(api_version="v2").liveness,
        ),
        (
            get_liveness_router,
            "test",
            get_model_server_urls(api_version="test").liveness,
        ),
        (
            get_readiness_router,
            "v2",
            get_model_server_urls(api_version="v2").readiness,
        ),
        (
            get_readiness_router,
            "test",
            get_model_server_urls(api_version="test").readiness,
        ),
    ],
)
def test_get_routers(get_router_method, test_api_version, test_route_url_expected):
    """Tests the following router creation utility methods
    - get_root_router
    - get_liveness_router
    - get_readiness_router
    and validates the url paths against the (previously tested) get_model_server_urls outputs"""

    test_router = get_router_method(api_version=test_api_version)
    test_route_url_actual = test_router.routes[0].path

    assert test_route_url_actual == test_route_url_expected


@pytest.mark.parametrize(
    "test_served_model_class, test_model_endpoint_type, test_api_version",
    [
        (
            ServedModel,
            ServedModelMethods().predict,
            "v2",
        ),
        (
            ServedModel,
            ServedModelMethods().predict,
            "test",
        ),
        (
            ServedModel,
            ServedModelMethods().bio,
            "v2",
        ),
        (
            ServedModel,
            ServedModelMethods().bio,
            "test",
        ),
        (
            TestServedModel,
            ServedModelMethods().predict,
            "v2",
        ),
        (
            TestServedModel,
            ServedModelMethods().predict,
            "test",
        ),
        (
            TestServedModel,
            ServedModelMethods().bio,
            "v2",
        ),
        (
            TestServedModel,
            ServedModelMethods().bio,
            "test",
        ),
    ],
)
def test_get_model_routers(
    test_served_model_class, test_model_endpoint_type, test_api_version, test_model_name
):
    """Tests the following router creation utility methods
    - get_model_predict_router
    - get_model_bio_router
    and validates
    - the url paths against the (previously tested) get_model_server_urls outputs
    - the response model against the data model attributes of a TestServedModel instance
    """

    test_served_model = test_served_model_class(name=test_model_name)

    test_urls = get_model_server_urls(
        api_version=test_api_version, model_name=test_model_name
    )

    if test_model_endpoint_type == ServedModelMethods().predict:
        test_route_url_expected = test_urls.model_predict
        test_model_router = get_model_predict_router(
            model=test_served_model, api_version=test_api_version
        )

        test_response_model_expected = test_served_model.predict_response_model

    elif test_model_endpoint_type == ServedModelMethods().bio:
        test_route_url_expected = test_urls.model_bio
        test_model_router = get_model_bio_router(
            model=test_served_model, api_version=test_api_version
        )

        test_response_model_expected = test_served_model.bio_response_model

    test_route_url_actual = test_model_router.routes[0].path
    test_route_response_model_actual = test_model_router.routes[0].response_model

    assert test_route_url_actual == test_route_url_expected
    assert test_route_response_model_actual == test_response_model_expected
