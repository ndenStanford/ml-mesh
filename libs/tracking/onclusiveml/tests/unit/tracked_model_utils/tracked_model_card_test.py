# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking.tracked_model_utils import (
    TrackedModelCard,
    TrackedModelTestFiles,
)


@pytest.mark.parametrize(
    "inputs,inference_params,predictions,model_type,model_artifact_attribute_path",
    [
        (
            "inputs",
            "inference_params",
            "predictions",
            "base",
            "artifacts",
        ),
        (
            "inputs",
            "inference_params",
            "predictions",
            "trained",
            "artifacts",
        ),
        (
            "inputs",
            "inference_params",
            "predictions",
            "compiled",
            "artifacts",
        ),
    ],
)
def from__init___test(
    inputs,
    inference_params,
    predictions,
    model_type,
    model_artifact_attribute_path,
    # model_loader,
):

    # create model card
    tracked_model_test_files = TrackedModelTestFiles(
        inputs=inputs, inference_params=inference_params, predictions=predictions
    )
    tracked_model_card = TrackedModelCard(
        model_type=model_type,
        model_artifact_attribute_path=model_artifact_attribute_path,
        model_test_files=tracked_model_test_files,
    )

    # TrackedModelCard attributes
    assert (
        tracked_model_card.model_artifact_attribute_path
        == model_artifact_attribute_path
    )
    assert tracked_model_card.model_type == model_type

    # TrackedModelTestFiles attributes
    assert tracked_model_card.model_test_files.inputs == inputs
    assert tracked_model_card.model_test_files.inference_params == inference_params
    assert tracked_model_card.model_test_files.predictions == predictions
