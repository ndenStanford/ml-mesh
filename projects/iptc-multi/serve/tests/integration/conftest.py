"""Conftest."""

# Standard Library
from typing import List

# 3rd party libraries
import pytest
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.serving.rest.serve import ServingParams

# Source
from src.serve.__main__ import model_server
from src.serve.schemas import BioResponseSchema


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
    return "Call functions to generate hash signatures for each article"


@pytest.fixture
def test_inference_params() -> str:
    """Predict input fixture."""
    return {"language": "en", "shingle_list": 5, "threshold": 0.6, "num_perm": 128}


@pytest.fixture
def test_expected_predict_output() -> List[str]:
    """Expected predict output fixture."""
    return {
        "version": 1,
        "data": {
            "identifier": None,
            "namespace": "iptc-multi",
            "attributes": {
                "iptc_topic": [
                    {
                        "label": "science and technology",
                        "score": 0.994,
                        "mediatopic_id": "13000000",
                    },
                    {
                        "label": "science and technology > natural science",
                        "score": 0.993,
                        "mediatopic_id": "20000717",
                    },
                    {
                        "label": "science and technology > natural science > biology",
                        "score": 0.47,
                        "mediatopic_id": "20000719",
                    },
                    {
                        "label": "science and technology > natural science > astronomy",
                        "score": 0.186,
                        "mediatopic_id": "20000718",
                    },
                    {
                        "label": "science and technology > natural science > physics",
                        "score": 0.114,
                        "mediatopic_id": "20000731",
                    },
                ]
            },
        },
    }


@pytest.fixture
def test_expected_bio_output():
    """Test expected bio output."""
    return BioResponseSchema.from_data(
        version=1,
        namespace="lsh",
        attributes={"model_name": "lsh"},
    )
