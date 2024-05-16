"""ServedModel tests."""

# Standard Library
from unittest.mock import MagicMock, patch

# 3rd party libraries
import pytest

# Source
from src.serve.schemas import PredictRequestSchema, PredictResponseSchema
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
    "payload, mock_return_values, expected_response",
    [
        (
            {
                "data": {
                    "identifier": None,
                    "namespace": "iptc-multi",
                    "attributes": {"content": "advanced science content"},
                    "parameters": {},
                }
            },
            {
                "combined": {},
                "processed": {},
                "postprocessed": [
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
                ],
            },
            {
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
            },
        )
    ],
)
@patch("src.serve.served_model.ServedIPTCMultiModel._postprocess_predictions")
@patch("src.serve.served_model.ServedIPTCMultiModel._process_combined_predictions")
@patch("src.serve.served_model.ServedIPTCMultiModel._get_combined_prediction")
def test_predict(
    mock_get_combined_prediction,
    mock_process_combined_predictions,
    mock_postprocess_predictions,
    payload,
    mock_return_values,
    expected_response,
):
    """Test the predict method processes inputs correctly."""
    model = ServedIPTCMultiModel()
    model.load()  # Sets the model to ready
    request_schema = PredictRequestSchema(**payload)

    mock_get_combined_prediction.return_value = mock_return_values["combined"]
    mock_process_combined_predictions.return_value = mock_return_values["processed"]
    mock_postprocess_predictions.return_value = mock_return_values["postprocessed"]

    response = model.predict(request_schema)

    assert isinstance(
        response, PredictResponseSchema
    ), "The response should be an instance of PredictResponseSchema"
    response_data = [
        {"label": t.label, "score": t.score, "mediatopic_id": t.mediatopic_id}
        for t in response.data.attributes.iptc_topic
    ]
    assert (
        response_data == expected_response["data"]["attributes"]["iptc_topic"]
    ), "The response data does not match the expected results"


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
