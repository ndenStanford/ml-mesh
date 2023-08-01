# """Test predict."""

# 3rd party libraries
import pytest
from fastapi import status


input = (
    """Call functions to generate hash signatures for each article""",  # noqa: E501
)


@pytest.mark.parametrize("input", input)
class TestParametrized:
    def test_lsh(self, test_client, input):
        """Test prediction endpoint."""
        response = test_client.post(
            "/v1/lsh/predict",
            json={
                "content": input,
                "language": "en",
                "shingle_list": 5,
                "threshold": 0.6,
                "num_perm": 128,
                "weights": (0.5, 0.5),
            },
        )
        assert len(response.json()["signature"]) > 0


input = (None,)  # noqa: E501


@pytest.mark.parametrize("input", input)
class TestParametrizedEmpty:
    def test_invalid_input(self, test_client, input):
        """Test prediction endpoint."""
        response = test_client.post(
            "/v1/lsh/predict",
            json={
                "content": input,
                "language": "en",
                "shingle_list": 5,
                "threshold": 0.6,
                "num_perm": 128,
                "weights": (0.5, 0.5),
            },
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
