"""Server functional tests."""

# 3rd party libraries
import pytest
import requests

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8000/iptc-multi/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/iptc-multi/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/iptc-multi/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_name") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        # Test case for an unsupported language (invalid language code)
        (
            {
                "data": {
                    "namespace": "iptc-multi",
                    "attributes": {"content": "crime"},  # noqa
                    "parameters": {"language": "xyz"},
                }
            },
            {
                "status": 422,
                "detail": "The language reference 'xyz' could not be mapped",
            },
        ),
        # Test case for an supported language
        (
            {
                "data": {
                    "namespace": "iptc-multi",
                    "attributes": {"content": "crime"},  # noqa
                    "parameters": {"language": "en"},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc-multi",
                    "attributes": {
                        "iptc_topic": [
                            {
                                "label": "crime, law and justice > crime > homicide",
                                "score": 0.995,
                                "mediatopic_id": "20000099",
                            },
                            {
                                "label": "crime, law and justice",
                                "score": 0.985,
                                "mediatopic_id": "02000000",
                            },
                            {
                                "label": "crime, law and justice > crime",
                                "score": 0.971,
                                "mediatopic_id": "20000082",
                            },
                        ]
                    },
                },
            },
        ),
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/iptc-multi/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
