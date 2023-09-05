"""Conftests."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.rest.serve import ModelServer, ServingParams


@pytest.fixture
def test_model_server():
    """Test model server."""
    test_serving_params = ServingParams(
        add_liveness=True,
        add_readiness=True,
        add_model_predict=False,
        add_model_bio=False,
        api_version="v1",
    )
    model_server = ModelServer(configuration=test_serving_params)
    return model_server
