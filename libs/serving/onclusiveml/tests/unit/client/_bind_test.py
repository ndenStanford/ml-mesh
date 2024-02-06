"""Test bind."""

# Standard Library
from typing import Callable
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.serialization import JsonApiSchema
from onclusiveml.serving.client._bind import bind


class RequestAttributes(JsonApiSchema):
    """Test request attributes."""

    attribute1: str
    attribute2: float


class ResponseAttributes(JsonApiSchema):
    """Test response attributes."""

    attribute3: str


class RequestParameters(JsonApiSchema):
    """Test request parameters."""

    parameter1: float


@pytest.mark.parametrize(
    "namespace, version, method, endpoint", [("test", 1, "GET", "test")]
)
def test_bind_init(namespace, version, method, endpoint):
    """Test bind init."""
    api = bind(
        namespace=namespace,
        version=version,
        method=method,
        endpoint=endpoint,
        request_attributes_schema=RequestAttributes,
        request_parameters_schema=RequestParameters,
        response_attributes_schema=ResponseAttributes,
    )

    assert isinstance(api, Callable)


@pytest.mark.parametrize(
    "namespace, version, method, endpoint, attribute1, attribute2, parameter1, attribute3",
    [
        ("test", 12, "GET", "test", "attribute1", 1, 1.2, "attribute3"),
        ("model_name", 2, "POST", "predict", "attr1", 100, 0.9, "attr3"),
    ],
)
@patch("requests.request")
def test_bind_call(
    mock_request,
    namespace,
    version,
    method,
    endpoint,
    attribute1,
    attribute2,
    parameter1,
    attribute3,
):
    """Test bind call."""

    class TestClient:
        """test cient."""

        def __init__(
            self,
            host: str,
            api_key: str,
            api_key_header: str = "x-api-key",
            secure: bool = True,
        ) -> None:
            self.protocol = "https" if secure else "http"
            self.host = host
            self.api_key_header = api_key_header
            self.api_key = api_key

        test = bind(
            namespace=namespace,
            version=version,
            method=method,
            endpoint=endpoint,
            request_attributes_schema=RequestAttributes,
            request_parameters_schema=RequestParameters,
            response_attributes_schema=ResponseAttributes,
        )

    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": namespace,
            "attributes": {"attribute3": attribute3},
        },
    }

    client = TestClient(host="dummy.host.com", api_key="")

    assert isinstance(client.test, Callable)

    client.test(attribute1=attribute1, attribute2=attribute2, parameter1=parameter1)

    mock_request.assert_called_with(
        method,
        f"https://dummy.host.com/{namespace}/v{version}/{endpoint}",
        headers={"x-api-key": "", "content-type": "application/json"},
        json={
            "data": {
                "identifier": None,
                "namespace": namespace,
                "attributes": {"attribute1": attribute1, "attribute2": attribute2},
                "parameters": {"parameter1": parameter1},
            }
        },
    )
