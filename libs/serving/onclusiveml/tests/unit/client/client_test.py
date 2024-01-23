"""Client test."""

# Standard Library
from typing import Callable
from unittest.mock import patch

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.serving.client import OnclusiveApiClient


@pytest.mark.parametrize(
    "host, api_key",
    [
        ("example.com", ""),
        ("internal.api.ml.stage.onclusive.com", "aa-bbbbbbbbbbbbbbb"),
    ],
)
def test_client_init(host, api_key):
    """Test client initialization."""
    client = OnclusiveApiClient(host=host, api_key=api_key)

    assert client.host == host
    assert client.api_key == api_key


@pytest.mark.parametrize(
    "host, api_key, api",
    [
        ("example.com", "", "entity_linking"),
        ("internal.api.ml.stage.onclusive.com", "aa-bbbbbbbbbbbbbbb", "ner"),
    ],
)
def test_client_getiitem(host, api_key, api):
    """Test client initialization."""
    client = OnclusiveApiClient(host=host, api_key=api_key)

    assert isinstance(client[api], Callable)


@pytest.mark.parametrize(
    "host, api_key, api, request_json, response_json",
    [
        (
            "example.com",
            "",
            "entity_linking",
            {
                "content": "Onclusive is a media monitoring company",
                "lang": "en",
                "entities": [],
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "entity-linking",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Onclusive",
                                "score": 0.9571336805820465,
                                "sentence_index": 0,
                                "wiki_link": None,
                            }
                        ]
                    },
                },
            },
        ),
        (
            "example.com",
            "",
            "ner",
            {
                "content": "Onclusive is a media monitoring company",
                "language": "en",
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "ner",
                    "attributes": {
                        "entities": [
                            {
                                "entity_type": "ORG",
                                "entity_text": "Onclusive",
                                "score": 0.8461078107357025,
                                "sentence_index": 0,
                                "start": 0,
                                "end": 9,
                            }
                        ]
                    },
                },
            },
        ),
    ],
)
@patch("requests.request")
def test_client_requests(mock_request, host, api_key, api, request_json, response_json):
    """Test client initialization."""
    client = OnclusiveApiClient(host=host, api_key=api_key)

    mock_request.return_value.status_code = 200
    mock_request.return_value.json.return_value = response_json

    response = client[api](**request_json)

    assert response.dict() == response_json
