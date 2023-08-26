"""Model server tests."""

# Standard Library
import time

# 3rd party libraries
import pytest
from served_model_test import TestServedModel

# Internal libraries
from onclusiveml.serving.rest.serve import (
    FastAPISettings,
    ModelServer,
    ServedModel,
    ServingParams,
)
from onclusiveml.serving.rest.serve.server_models import ServedModelMethods


@pytest.mark.parametrize(
    "test_add_liveness, test_add_readiness, test_api_version, test_api_name",
    [
        (False, False, "v1", "api_name_1"),
        (False, True, "v2", "api_name_2"),
        (True, True, "v3", "api_name_3"),
        (True, False, "v4", "api_name_4"),
    ],
)
def test_model_server___init__no_model(
    test_add_liveness, test_add_readiness, test_api_version, test_api_name
):
    """Tests initialization of the ModelServer class without passing a model, validating
    - toggling of liveness endpoint
    - toggling of readiness endpoint
    - capturing of api name and api version
    - the configuration attribute capturing the serving params"""

    test_serving_params = ServingParams(
        add_liveness=test_add_liveness,
        add_readiness=test_add_readiness,
        add_model_predict=False,
        add_model_bio=False,
        api_version=test_api_version,
        fastapi_settings=FastAPISettings(name=test_api_name),
    )
    test_model_server = ModelServer(configuration=test_serving_params, model=None)
    # --- check probe route building behaviour
    test_versioned_model_server_routes = [
        route
        for route in test_model_server.router.routes
        if route.path.startswith(f"/{test_api_version}")
    ]
    test_has_liveness_route = [
        route for route in test_versioned_model_server_routes if route.name == "live"
    ]
    test_has_readiness_route = [
        route for route in test_versioned_model_server_routes if route.name == "ready"
    ]
    # check that liveness endpoint has been built/not built following the specs
    assert bool(test_has_liveness_route) == test_add_liveness
    # check that liveness endpoint has been built/not built following the specs
    assert bool(test_has_readiness_route) == test_add_readiness
    # --- check api name
    assert test_model_server.extra["name"] == test_api_name
    # --- check configuration attribute
    assert test_model_server.configuration == test_serving_params


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
def test_model_server___init__with_model(
    test_served_model_class,
    test_add_model_predict,
    test_add_model_bio,
    test_api_version,
    test_on_startup,
    test_model_name,
):
    """Tests initialization of the ModelServer class without passing a model, validating
    - toggling of liveness endpoint
    - toggling of readiness endpoint
    - capturing of api name and api version
    - the configuration attribute capturing the serving params"""

    test_serving_params = ServingParams(
        add_liveness=False,
        add_readiness=False,
        add_model_predict=test_add_model_predict,
        add_model_bio=test_add_model_bio,
        api_version=test_api_version,
    )

    test_model_server = ModelServer(
        configuration=test_serving_params,
        model=test_served_model_class(name=test_model_name),
        on_startup=[test_on_startup],
    )
    # --- check model route building behaviour
    test_versioned_model_server_routes = [
        route
        for route in test_model_server.router.routes
        if route.path.startswith(f"/{test_api_version}")
    ]
    test_has_predict_route = [
        route
        for route in test_versioned_model_server_routes
        if route.name == ServedModelMethods().predict
    ]
    test_has_bio_route = [
        route
        for route in test_versioned_model_server_routes
        if route.name == ServedModelMethods().bio
    ]
    # check that liveness endpoint has been built/not built following the specs
    assert bool(test_has_predict_route) == test_add_model_predict
    # check that liveness endpoint has been built/not built following the specs
    assert bool(test_has_bio_route) == test_add_model_bio
