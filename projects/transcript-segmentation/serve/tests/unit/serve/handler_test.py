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
    transcript_segmentation_inference[0] == expected_output["start_time"]
    assert transcript_segmentation_inference[1] == expected_output["end_time"]
    assert transcript_segmentation_inference[2] == expected_output["input_truncated"]
