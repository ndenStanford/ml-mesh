"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch

# Source
from src.serve.handler import TranscriptSegmentationHandler

_service = TranscriptSegmentationHandler()


@patch("requests.post")
def test_handler___call___(
    mock_post,
    transcript_input,
    transcript_keywords,
    transcript_offset,
    model_card,
    expected_output,
):
    """Test the inference function in transcript segmentation handler."""
    mock_post.return_value = model_card

    transcript_segmentation_inference = _service(
        word_transcript=transcript_input,
        keywords=transcript_keywords,
        offset_start_buffer=transcript_offset[0],
        offset_end_buffer=transcript_offset[1],
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
    assert transcript_segmentation_inference[4] == expected_output["segment"]
    assert transcript_segmentation_inference[2] == expected_output["segment title"]
    assert transcript_segmentation_inference[3] == expected_output["segment summary"]
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
