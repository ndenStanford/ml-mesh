# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import ModelServer, ServingParams


@pytest.fixture
def test_model_name():
    return "test_animal_classifier"


@pytest.fixture
def setup_model_server(
    test_served_model_class,
    test_add_model_predict,
    test_add_model_bio,
    test_api_version,
    test_on_startup,
    test_model_name,
):
    test_serving_params = ServingParams(
        add_liveness=False,
        add_readiness=False,
        add_model_predict=test_add_model_predict,
        add_model_bio=test_add_model_bio,
        api_version=test_api_version,
    )

    model_server = ModelServer(
        configuration=test_serving_params,
        model=test_served_model_class(name=test_model_name),
        on_startup=[test_on_startup],
    )
    return model_server
