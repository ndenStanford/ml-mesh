"""Test routes."""

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest
from fastapi import status

# Source
from src.predict import keybert


def test_health_route(test_client):
    """Test health endpoint."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "OK"


@pytest.mark.parametrize(
    "input, expected_output, prediction",
    [
        (
            "Investigate the use of Evidently for live model drift",
            {
                "keywords": [
                    "live model drift",
                    "model drift",
                    "evidently live model",
                    "live model",
                    "drift",
                    "model",
                    "use evidently live",
                    "evidently live",
                    "live",
                    "investigate use evidently",
                    "use evidently",
                    "investigate use",
                    "evidently",
                    "investigate",
                    "use",
                ],
                "probs": [
                    0.909,
                    0.8568,
                    0.714,
                    0.6817,
                    0.64,
                    0.5706,
                    0.5098,
                    0.3791,
                    0.3758,
                    0.3057,
                    0.2835,
                    0.2606,
                    0.2438,
                    0.2041,
                    0.2003,
                ],
            },
            [
                ["live model drift", 0.909],
                ["model drift", 0.8568],
                ["evidently live model", 0.714],
                ["live model", 0.6817],
                ["drift", 0.64],
                ["model", 0.5706],
                ["use evidently live", 0.5098],
                ["evidently live", 0.3791],
                ["live", 0.3758],
                ["investigate use evidently", 0.3057],
                ["use evidently", 0.2835],
                ["investigate use", 0.2606],
                ["evidently", 0.2438],
                ["investigate", 0.2041],
                ["use", 0.2003],
            ],
        )
    ],
)
@patch.object(keybert.KeybertHandler, "inference")
def test_predict(mock_service, test_client, input, expected_output, prediction):
    """Test prediction endpoint."""
    mock_service.return_value = prediction
    response = test_client.post(
        "/v1/keywords/predict",
        json={
            "content": input,
            "keyphrase_ngram_range": (1, 3),
            "use_maxsum": False,
            "diversity": 0.35,
            "nr_candidates": 20,
            "top_n": 20,
        },
    )
    mock_service.assert_called()
    assert response.json() == expected_output
