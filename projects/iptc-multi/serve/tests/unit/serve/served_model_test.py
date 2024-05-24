"""ServedModel tests."""

# Standard Library
from unittest.mock import MagicMock, patch

# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedIPTCMultiModel


def test_initialization():
    """Test the initialization of ServedIPTCMultiModel."""
    model = ServedIPTCMultiModel()
    assert model.name == "iptc-multi"
    assert model.ready is False


@patch("src.serve.served_model.OnclusiveApiClient")
def test_load(api_client_mock):
    """Test the load function sets the model to ready and initializes the client."""
    model = ServedIPTCMultiModel()
    model.load()
    assert model.ready
    assert model.model == api_client_mock


@pytest.mark.parametrize(
    "iptc_response, expected_result",
    [
        (None, False),  # Case when at least one model failed
        ([], True),  # Case when all models return empty array due to empty content
        (
            {
                "version": 1,
                "data": {
                    "identifier": None,
                    "namespace": "iptc-00000000",
                    "attributes": {
                        "iptc": [
                            {"label": "economy, business and finance", "score": 0.9871},
                            {"label": "conflict, war and peace", "score": 0.0056},
                            {"label": "crime, law and justice", "score": 0.0023},
                            {"label": "science and technology", "score": 0.002},
                            {"label": "labour", "score": 0.0009},
                            {
                                "label": "disaster, accident and emergency incident",
                                "score": 0.0005,
                            },
                            {"label": "lifestyle and leisure", "score": 0.0004},
                            {"label": "weather", "score": 0.0004},
                            {"label": "politics", "score": 0.0002},
                            {
                                "label": "arts, culture, entertainment and media",
                                "score": 0.0001,
                            },
                            {"label": "environment", "score": 0.0001},
                            {"label": "health", "score": 0.0001},
                            {"label": "society", "score": 0.0001},
                            {"label": "sport", "score": 0.0001},
                            {"label": "education", "score": 0.0},
                            {"label": "religion", "score": 0.0},
                        ]
                    },
                },
            },
            True,
        ),  # Case when all models respond as expected
    ],
)
@patch("src.serve.served_model.ServedIPTCMultiModel._get_current_model")
@patch("src.serve.served_model.ServedIPTCMultiModel._create_client")
def test_are_all_models_live(
    create_client_mock, get_current_model_mock, iptc_response, expected_result
):
    """Test the are_all_models_live method to ensure it correctly assesses model livenes."""
    model = ServedIPTCMultiModel()
    model.load()

    api_response = MagicMock()
    api_response.attributes.iptc = iptc_response

    create_client_mock.return_value = MagicMock()
    get_current_model_mock.return_value = lambda *args, **kwargs: api_response

    result = model.are_all_models_live()

    assert (
        result == expected_result
    ), f"Expected are_all_models_live to return {expected_result} but got {result}"

    assert create_client_mock.called, "Failed to call _create_client"
    assert get_current_model_mock.called, "Failed to call _get_current_model"
