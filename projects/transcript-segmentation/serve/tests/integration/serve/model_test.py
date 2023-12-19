"""Prediction model tests."""

# 3rd party libraries
import pytest

# Source
from src.serve.model import ServedTranscriptSegmentationModel
from src.serve.schemas import PredictRequestSchema
from src.settings import get_settings


settings = get_settings()


@pytest.mark.order(1)
def test_served_transcript_segmentation_model__init__():
    """Tests the constructor of the ServedTranscriptSegmentationModel."""
    ServedTranscriptSegmentationModel()


@pytest.mark.order(2)
def test_served_transcript_segmentation_model_load():
    """Tests the constructor of the ServedTranscriptSegmentationModel."""
    served_transcript_segmentation_model = ServedTranscriptSegmentationModel()
    assert not served_transcript_segmentation_model.is_ready()

    served_transcript_segmentation_model.load()

    assert served_transcript_segmentation_model.is_ready()


@pytest.mark.order(3)
def test_served_transcript_segmentation_model_predict(
    test_predict_input,
    test_inference_params,
    test_expected_predict_output,
    test_predict_keyword,
):
    """Tests the fully initialized and loaded ServedTranscriptSegmentationModel's predict method."""
    served_transcript_segmentation_model = ServedTranscriptSegmentationModel()
    served_transcript_segmentation_model.load()

    test_input = PredictRequestSchema.from_data(
        namespace=settings.model_name,
        parameters=test_inference_params,
        attributes={"transcript": test_predict_input, "keyword": test_predict_keyword},
    )

    test_actual_predict_output = served_transcript_segmentation_model.predict(
        test_input
    )

    assert test_actual_predict_output == test_expected_predict_output


@pytest.mark.order(3)
def test_served_transcript_segmentation_model_bio(test_expected_bio_output):
    """Tests the fully initialized and loaded ServedTranscriptSegmentationModel's bio method."""
    served_transcript_segmentation_model = ServedTranscriptSegmentationModel()

    served_transcript_segmentation_model.load()

    test_actual_bio_output = served_transcript_segmentation_model.bio()

    assert test_actual_bio_output == test_expected_bio_output
