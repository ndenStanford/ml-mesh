"""Unit test inference and aggregate."""

# isort: skip_file

# Standard Library
from unittest.mock import patch

# 3rd party libraries
import pytest

# Source
from src.serve.handler import TranscriptSegmentationHandler
from src.serve.exceptions import PromptBackendException, StructuredOutputException

_service = TranscriptSegmentationHandler()


@patch("requests.post")
def test_handler___call___(
    mock_post,
    transcript_input,
    transcript_keywords,
    transcript_offset,
    transcript_country,
    mock_response,
    expected_output,
):
    """Test the inference function in transcript segmentation handler."""
    mock_post.return_value = mock_response

    transcript_segmentation_inference = _service(
        word_transcript=transcript_input,
        keywords=transcript_keywords,
        offset_start_buffer=transcript_offset[0],
        offset_end_buffer=transcript_offset[1],
        country=transcript_country[1],
    )
    assert transcript_segmentation_inference[0][0] == expected_output["start_time"]
    assert transcript_segmentation_inference[0][1] == expected_output["end_time"]
    assert (
        transcript_segmentation_inference[1][0]
        == expected_output["transcript_start_time"]
    )
    assert (
        transcript_segmentation_inference[1][1]
        == expected_output["transcript_end_time"]
    )
    assert transcript_segmentation_inference[4] == expected_output["related_segment"]
    assert transcript_segmentation_inference[2] == expected_output["segment_title"]
    assert transcript_segmentation_inference[3] == expected_output["segment_summary"]
    assert transcript_segmentation_inference[5] == expected_output["ad"]


def test_handler_preprocessing(transcript_input, expected_preprocessing_output):
    """Test preprocessing function."""
    res = _service.preprocess_transcript(transcript_input)
    assert res == expected_preprocessing_output


def test_handler_preprocessing_abbrv(
    transcript_input_abbrv, expected_preprocessing_output_abbrv
):
    """Test preprocessing function where input has abbreviation."""
    res = _service.preprocess_transcript(transcript_input_abbrv)
    assert res == expected_preprocessing_output_abbrv


@patch("requests.post")
def test_handler_ad(mock_post, ad_input, transcript_keywords, mock_ad_response_yes):
    """Test ad detect."""
    mock_post.return_value = mock_ad_response_yes

    res = _service.ad_detect(ad_input, transcript_keywords)
    assert res is True


@patch("requests.post")
def test_handler_ad_none_output(
    mock_post, ad_input, transcript_keywords, mock_ad_response_none
):
    """Test ad detect."""
    mock_post.return_value = mock_ad_response_none

    res = _service.ad_detect(ad_input, transcript_keywords)
    assert res is False


@patch("requests.post")
def test_handler_prompt_backend_exception(
    mock_post,
    transcript_input,
    transcript_keywords,
    transcript_offset,
    transcript_country,
    mock_response_upstream_error,
):
    """Test the exception handling."""
    mock_post.return_value = mock_response_upstream_error

    with pytest.raises(PromptBackendException):
        _ = _service(
            word_transcript=transcript_input,
            keywords=transcript_keywords,
            offset_start_buffer=transcript_offset[0],
            offset_end_buffer=transcript_offset[1],
            country=transcript_country[1],
        )


@patch("requests.post")
def test_handler_structured_output_exception(
    mock_post,
    transcript_input,
    transcript_keywords,
    transcript_offset,
    transcript_country,
    mock_response_structured_output_error,
):
    """Test the exception handling."""
    mock_post.return_value = mock_response_structured_output_error

    with pytest.raises(StructuredOutputException):
        _ = _service(
            word_transcript=transcript_input,
            keywords=transcript_keywords,
            offset_start_buffer=transcript_offset[0],
            offset_end_buffer=transcript_offset[1],
            country=transcript_country[1],
        )
