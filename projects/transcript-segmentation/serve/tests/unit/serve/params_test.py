"""Unit test inference and aggregate."""
# isort: skip_file

# Standard Library
from unittest.mock import patch

# Source
from src.serve.transcript_segmentation import TranscriptSegmentationHandler

_service = TranscriptSegmentationHandler()


@patch("requests.post")
def test_handler_predict(
    mock_post, transcript_input, transcript_keyword, model_card, expected_output
):
    """Test the inference function in transcript segmentation handler."""
    mock_post.return_value = model_card

    transcript_segmentation_inference = _service.predict(
        word_transcript=transcript_input,
        keyword=transcript_keyword,
    )
    assert (
        transcript_segmentation_inference[0] == expected_output["segmented_transcript"]
    )
    assert transcript_segmentation_inference[1] == expected_output["output_truncated"]
    assert transcript_segmentation_inference[2] == expected_output["input_truncated"]
