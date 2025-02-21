"""Server utils tests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging.constants import LOG_LEVELS, OnclusiveService
from onclusiveml.serving.rest.serve import (
    BetterStackSettings,
    ServedModel,
    get_liveness_router,
    get_logging_config,
    get_model_bio_router,
    get_model_predict_router,
    get_readiness_router,
)
from onclusiveml.serving.rest.serve.server_models import ServedModelMethods
from onclusiveml.serving.rest.serve.server_utils import (
    TEST_MODEL_NAME,
    get_model_server_urls,
)


@pytest.mark.parametrize(
    "test_kwargs,root_url_expected,liveness_url_expected,readiness_url_expected,predict_url_expected,bio_url_expected",  # noqa: E501
    [
        (
            {},  # test defaults
            "/no_model/v1/",
            "/no_model/v1/live",
            "/no_model/v1/ready",
            "/no_model/v1/predict",
            "/no_model/v1/bio",
        ),
        (
            {"api_version": "test-version", "model_name": "test-model"},
            "/test-model/test-version/",
            "/test-model/test-version/live",
            "/test-model/test-version/ready",
            "/test-model/test-version/predict",
            "/test-model/test-version/bio",
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
    """Tests the utility method get_model_server_urls to produce correctly parametrized urls.

    - with & without specified api version
    - with & without a model
    """
    test_urls = get_model_server_urls(**test_kwargs)

    assert test_urls.root == root_url_expected
    assert test_urls.liveness == liveness_url_expected
    assert test_urls.readiness == readiness_url_expected
    assert test_urls.model_predict == predict_url_expected
    assert test_urls.model_bio == bio_url_expected


@pytest.mark.parametrize(
    "get_router_method, test_api_version, test_route_url_expected",
    [
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
    """Test router creation helpers.

    Notes:
        Tests the following router creation utility methods
        - get_liveness_router
        - get_readiness_router
        and validates the url paths against the (previously tested) get_model_server_urls outputs
    """
    if get_router_method == get_liveness_router:
        test_router = get_router_method(
            api_version=test_api_version,
            betterstack_settings=BetterStackSettings(),
            model=ServedModel(TEST_MODEL_NAME),
        )
    else:
        test_router = get_router_method(
            api_version=test_api_version, model=ServedModel(TEST_MODEL_NAME)
        )

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
            pytest.lazy_fixture("get_test_served_model"),
            ServedModelMethods().predict,
            "v2",
        ),
        (
            pytest.lazy_fixture("get_test_served_model"),
            ServedModelMethods().predict,
            "test",
        ),
        (
            pytest.lazy_fixture("get_test_served_model"),
            ServedModelMethods().bio,
            "v2",
        ),
        (
            pytest.lazy_fixture("get_test_served_model"),
            ServedModelMethods().bio,
            "test",
        ),
    ],
)
def test_get_model_routers(
    test_served_model_class, test_model_endpoint_type, test_api_version, test_model_name
):
    """Model router tests.

    Notes:
        Tests the following router creation utility methods.
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


@pytest.mark.parametrize("service", OnclusiveService.values())
@pytest.mark.parametrize("level", LOG_LEVELS)
@pytest.mark.parametrize("json_format", [True, False])
def test_get_logging_config(service, level, json_format):
    """Tests the get_logging_config function."""
    get_logging_config(service, level, json_format)
