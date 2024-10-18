"""Server functional tests."""

# 3rd party libraries
import pytest
import requests
from pytest import approx

# Internal libraries
from onclusiveml.serving.rest.serve import (
    LivenessProbeResponse,
    ReadinessProbeResponse,
)


def test_model_server_liveness():
    """Tests the liveness endpoint of a ModelServer (not running) instance."""
    liveness_response = requests.get("http://serve:8000/visitor-estimation/v1/live")

    assert liveness_response.status_code == 200
    assert liveness_response.json() == LivenessProbeResponse().model_dump()


def test_model_server_readiness():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/visitor-estimation/v1/ready")

    assert readiness_response.status_code == 200
    assert readiness_response.json() == ReadinessProbeResponse().model_dump()


def test_model_server_bio():
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    readiness_response = requests.get("http://serve:8000/visitor-estimation/v1/bio")

    assert readiness_response.status_code == 200
    assert readiness_response.json()["data"]["attributes"].get("model_card") is not None


@pytest.mark.parametrize(
    "payload, expected_response",
    [
        (
            {
                "data": {
                    "namespace": "visitor-estimation",
                    "attributes": {
                        "input": [
                            {
                                "profileID": 2252,
                                "analyticsTimestamp": [
                                    "2016-08-12T00:00:00",
                                    "2016-08-11T00:00:00",
                                    "2016-08-13T00:00:00",
                                ],
                                "entityTimestamp": "2016-08-10T07:46:59",
                                "social": {
                                    "metadataTimestamp": [
                                        "2016-08-11T00:00:00",
                                        "2016-08-11T18:00:00",
                                        "2016-08-12T10:00:00",
                                    ],
                                    "fbLikes": [1000, 1000, 1000],
                                    "fbComments": [1000, 1000, 1000],
                                    "fbTotal": [1000, 1000, 1000],
                                    "fbShares": [1000, 1000, 1000],
                                    "linkedInShares": [1000, None, 1000],
                                    "googlePlusones": [1000, None, 1100],
                                    "twitterRetweets": [1000, 1000, 1200],
                                },
                                "wordCount": 500,
                                "domainLinkCount": 2,
                                "nonDomainLinkCount": 0,
                                "namedEntityCount": 3,
                                "relevance": 0.92,
                                "pagerank": 7.3,
                                "companySectorId": 16,
                                "typeCd": 3,
                                "category": 2,
                                "isSyndicateChild": False,
                                "isSyndicateParent": True,
                            }
                        ],
                    },
                    "parameters": {
                        "language": "en",
                    },
                }
            },
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "visitor-estimation",
                    "attributes": {
                        "predicted_visitors": [
                            1.4622888266898326,
                            1.29739670999407,
                            1.5491212546385245,
                        ],
                    },
                },
            },
        )
    ],
)
def test_model_server_prediction(payload, expected_response):
    """Tests the readiness endpoint of a ModelServer (not running) instance."""
    response = requests.post(
        "http://serve:8000/visitor-estimation/v1/predict",
        json=payload,
    )
    actual_response = response.json()
    actual_predictions = actual_response["data"]["attributes"]["predicted_visitors"]
    expected_predictions = expected_response["data"]["attributes"]["predicted_visitors"]
    # Assert predictions are approximately equal
    assert actual_predictions == approx(expected_predictions, rel=1)
    assert response.status_code == 200
    assert response.json() == expected_response
