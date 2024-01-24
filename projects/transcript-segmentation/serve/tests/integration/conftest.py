"""Conftest."""

# Standard Library
from typing import List

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.schemas import BioResponseSchema, PredictResponseSchema
from src.serve.server import model_server


@pytest.fixture
def test_serving_params():
    """Serving params fixture."""
    return ServingParams()


@pytest.fixture
def test_client():
    """Client fixture."""
    return TestClient(model_server)


@pytest.fixture
def test_predict_input() -> str:
    """Predict input fixture."""
    return [
        {
            "start_time": 1701127816000.0,
            "content": "Watch 'a Day's Work,' in their unreliability.",
        },
        {
            "start_time": 1701127820000.0,
            "content": "They're arguably the most versatile ai technique that's ever been developed, but they're also the least reliable ai technique that's ever gone mainstream.",  # noqa: E501
        },
        {
            "start_time": 1701127828000.0,
            "content": '[bright music] [logo whooshes] - Hello and welcome to "gzero World.',  # noqa: E501
        },
        {
            "start_time": 1701127839000.0,
            "content": "I'm Ian Bremmer, and, today, we're talking about all things artificial intelligence, specifically generative ai, those chatbots like ChatGPT that you've surely heard about by now.",  # noqa: E501
        },
        {
            "start_time": 1701127849000.0,
            "content": "You know, the ones that can churn out a two-hour movie script or Picasso-style painting in just an instant.",  # noqa: E501
        },
    ]  # noqa: E501


@pytest.fixture
def test_predict_keyword() -> str:
    """Predict keyword fixture."""
    return ["Ai"]


@pytest.fixture
def test_inference_params() -> str:
    """Predict parameter fixture."""
    return {}


@pytest.fixture
def test_expected_predict_output() -> List[str]:
    """Expected predict output fixture."""
    return PredictResponseSchema.from_data(
        version=1,
        namespace="transcript-segmentation",
        attributes={
            "start_time": 1701127820000.0,
            "end_time": 1701127849000.0,
            "input_truncated": False,
        },
    )


@pytest.fixture
def test_expected_bio_output():
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="transcript-segmentation",
        attributes={"model_name": "transcript-segmentation"},
    )
