"""Server functional tests."""

# 3rd party libraries
import pytest
import requests
import sklearn

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


sklearn_version = sklearn.__version__
print("Scikit-learn version:", sklearn_version)


def test_model_server_root():
    """Tests the root endpoint of a ModelServer (not running) instance."""
    root_response = requests.get("http://serve:8000/content-scoring/v1/")

    assert root_response.status_code == 200


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/content-scoring/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().dict()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/content-scoring/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().dict()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/content-scoring/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "content-scoring",
                    "attributes": {
                        "dataframe": {
                            "pagerank": [3.299923, 9.1, 9.4],
                            "reach": [90, 2821568, 3614746],
                            "score": [628226.6, 4213572.0, 1601918.4],
                            "lang": [2.0, 2.0, 0.0],
                            "media_type": [3.0, 3.0, 3.0],
                            "label": [1.0, 1.0, 2.0],
                            "publication": [72.0, 69.0, 43.0],
                            "country": [1.0, 1.0, 2.0],
                            "is_copyrighted": [0.0, 0.0, 0.0],
                            "type_of_summary": [0.0, 0.0, 0.0],
                        }
                    },
                    "parameters": {},
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "content-scoring",
                    "attributes": {
                        "boolean_messages": ["rejected", "rejected", "rejected"]
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/content-scoring/v1/predict",
        json=payload,
    )

    assert response.status_code == 200
    # TODO: assert score close to expected
    assert response.json() == expected_response
