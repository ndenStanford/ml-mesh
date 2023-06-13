# 3rd party libraries
import pytest
import requests
from pydantic import BaseModel

# Internal libraries
from onclusiveml.serving.rest.params import (
    FastAPISettings,
    ServingParams,
    UvicornSettings,
)
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ModelServer,
    ReadinessProbeResponse,
)
from onclusiveml.serving.rest.serve.server_utils import (
    SERVING_LIVENESS_PROBE_URL,
    SERVING_READINESS_PROBE_URL,
    SERVING_ROOT_URL,
)


# from served_model_test import TestServedModel


class RootResponse(BaseModel):
    name: str


@pytest.mark.no_model
@pytest.mark.serve
def test_model_server__serve_no_model(test_api_version, test_port):

    test_serving_params = ServingParams(
        add_liveness=True,
        add_readiness=True,
        add_model_predict=False,
        add_model_bio=False,
        api_version=test_api_version,
        fastapi_settings=FastAPISettings(name="test-api"),
        uvicorn_settings=UvicornSettings(http_port=test_port),
    )

    test_model_server = ModelServer(configuration=test_serving_params, model=None)

    test_model_server.serve()


@pytest.mark.no_model
@pytest.mark.client
@pytest.mark.parametrize(
    "test_url_template, test_probe_response_model",
    [
        (SERVING_ROOT_URL, RootResponse),
        (SERVING_LIVENESS_PROBE_URL, LivenessProbeResponse),
        (SERVING_READINESS_PROBE_URL, ReadinessProbeResponse),
    ],
)
def test_model_server_client_no_model(
    test_api_version, test_port, test_url_template, test_probe_response_model
):
    # check liveness
    url = f"http://localhost:{test_port}" + test_url_template.format(
        api_version=test_api_version
    )

    response = requests.get(url)

    test_probe_response_model(**response.json())
