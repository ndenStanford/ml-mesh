"""Test predict."""

# 3rd party libraries
import pytest


@pytest.mark.parametrize(
    "input, expected_output",
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
        )
    ],
)
def test_predict(test_client, input, expected_output):
    """Test prediction endpoint."""
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
    assert response.json() == expected_output
