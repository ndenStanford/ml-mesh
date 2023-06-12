# 3rd party libraries
import pytest
from served_model_test import TestServedModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    ServedModel,
    create_model_endpoint,
    get_liveness_router,
    get_readiness_router,
    get_root_router,
)
from onclusiveml.serving.rest.serve.server_utils import (
    SERVING_LIVENESS_PROBE_URL,
    SERVING_ML_MODEL_BIO_URL,
    SERVING_ML_MODEL_PREDICT_URL,
    SERVING_READINESS_PROBE_URL,
    SERVING_ROOT_URL,
)


@pytest.mark.parametrize(
    "get_router_method, test_api_version, test_route_url_expected",
    [
        (get_root_router, "v2", SERVING_ROOT_URL.format(api_version="v2")),
        (get_root_router, "test", SERVING_ROOT_URL.format(api_version="test")),
        (
            get_liveness_router,
            "v2",
            SERVING_LIVENESS_PROBE_URL.format(api_version="v2"),
        ),
        (
            get_liveness_router,
            "test",
            SERVING_LIVENESS_PROBE_URL.format(api_version="test"),
        ),
        (
            get_readiness_router,
            "v2",
            SERVING_READINESS_PROBE_URL.format(api_version="v2"),
        ),
        (
            get_readiness_router,
            "test",
            SERVING_READINESS_PROBE_URL.format(api_version="test"),
        ),
    ],
)
def test_get_routers(get_router_method, test_api_version, test_route_url_expected):

    test_router = get_router_method(api_version=test_api_version)
    test_route_url_actual = test_router.routes[0].path

    assert test_route_url_actual == test_route_url_expected


@pytest.mark.parametrize(
    "test_served_model, test_endpoint, test_api_version, test_route_url_template",
    [
        (
            ServedModel,
            "predict",
            "v2",
            SERVING_ML_MODEL_PREDICT_URL,
        ),
        (
            ServedModel,
            "predict",
            "test",
            SERVING_ML_MODEL_PREDICT_URL,
        ),
        (
            ServedModel,
            "bio",
            "v2",
            SERVING_ML_MODEL_BIO_URL,
        ),
        (
            ServedModel,
            "bio",
            "test",
            SERVING_ML_MODEL_BIO_URL,
        ),
        (
            TestServedModel,
            "predict",
            "v2",
            SERVING_ML_MODEL_PREDICT_URL,
        ),
        (
            TestServedModel,
            "predict",
            "test",
            SERVING_ML_MODEL_PREDICT_URL,
        ),
        (
            TestServedModel,
            "bio",
            "v2",
            SERVING_ML_MODEL_BIO_URL,
        ),
        (
            TestServedModel,
            "bio",
            "test",
            SERVING_ML_MODEL_BIO_URL,
        ),
    ],
)
def test_create_model_endpoint(
    test_served_model,
    test_endpoint,
    test_api_version,
    test_route_url_template,
):

    test_route_url_expected = test_route_url_template.format(
        api_version=test_api_version, model_name=test_served_model.name
    )

    test_model_endpoint = create_model_endpoint(
        model=test_served_model, endpoint=test_endpoint, api_version=test_api_version
    )

    test_route_url_actual = test_model_endpoint.routes[0].path
    test_route_response_model_actual = test_model_endpoint.routes[0].response_model

    assert test_route_url_actual == test_route_url_expected

    if test_endpoint == "predict":
        test_response_model_expected = test_served_model.bio_response_model
    elif test_endpoint == "bio":
        test_response_model_expected = test_served_model.bio_response_model

    assert test_route_response_model_actual == test_response_model_expected
