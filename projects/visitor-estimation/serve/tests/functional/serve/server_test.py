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
                                "profile_id": 2252,
                                "analytics_timestamp": [
                                    "2016-08-12T00:00:00",
                                    "2016-08-11T00:00:00",
                                    "2016-08-13T00:00:00",
                                ],
                                "entity_timestamp": "2016-08-10T07:46:59",
                                "social": {
                                    "metadata_timestamp": [
                                        "2016-08-11T00:00:00",
                                        "2016-08-11T18:00:00",
                                        "2016-08-12T10:00:00",
                                    ],
                                    "fb_likes": [1000, 1000, 1000],
                                    "fb_comments": [1000, 1000, 1000],
                                    "fb_total": [1000, 1000, 1000],
                                    "fb_shares": [1000, 1000, 1000],
                                    "linkedIn_shares": [1000, None, 1000],
                                    "google_plusones": [1000, None, 1100],
                                    "twitter_retweets": [1000, 1000, 1200],
                                },
                                "word_count": 500,
                                "domain_link_count": 2,
                                "non_domain_link_count": 0,
                                "named_entity_count": 3,
                                "relevance": 0.92,
                                "page_rank": 7.3,
                                "company_sector_id": 16,
                                "type_cd": 3,
                                "category": 2,
                                "is_syndicate_child": False,
                                "is_syndicate_parent": True,
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
                            0.41421356237309503,
                            0.3660402567543955,
                            0.3660402567543955,
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
    assert actual_predictions == approx(expected_predictions, rel=10)
    assert response.status_code == 200
