"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch

# Source
from src.serve.handler import TranscriptSegmentationHandler

_service = TranscriptSegmentationHandler()


@patch("requests.post")
def test_handler___call___(
    mock_post, transcript_input, transcript_keywords, model_card, expected_output
):
    """Test the inference function in transcript segmentation handler."""
    mock_post.return_value = model_card

    transcript_segmentation_inference = _service(
        word_transcript=transcript_input,
        keywords=transcript_keywords,
    )
    assert transcript_segmentation_inference[0] == expected_output["start_time"]
    assert transcript_segmentation_inference[1] == expected_output["end_time"]


def test_handler_preprocessing(transcript_input, expected_preprocessing_output):
    """Test preprocessing function."""
    res = _service.preprocess_transcript(transcript_input)
    print(res)
    assert res == expected_preprocessing_output


def test_handler_preprocessing_abbrv(
    transcript_input_abbrv, expected_preprocessing_output_abbrv
):
    """Test preprocessing function where input has abbreviation."""
    res = _service.preprocess_transcript(transcript_input_abbrv)
    assert res == expected_preprocessing_output_abbrv
