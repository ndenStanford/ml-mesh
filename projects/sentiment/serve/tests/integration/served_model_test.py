# ML libs
import torch

# 3rd party libraries
import pytest

# Source
from src.serve.served_model import ServedSentModel
from src.serve.server_models import (
    BioResponseModel,
    PredictConfiguration,
    PredictInputContentModel,
    PredictionOutputContent,
    PredictRequestModel,
    PredictResponseModel,
)


@pytest.mark.order(1)
def test_served_sent_model__init__(test_served_model_artifacts):
    """Tests the constructor of the ServedSentModel, EXCLUDING the loading of genuine model
    artifacts from local disk"""

    ServedSentModel(served_model_artifacts=test_served_model_artifacts)


@pytest.mark.order(2)
def test_served_sent_model_load(test_served_model_artifacts):
    """Tests the constructor of the ServedSentModel, INCLUDING the loading of genuine model
    artifacts from local disk"""

    served_sent_model = ServedSentModel(
        served_model_artifacts=test_served_model_artifacts
    )

    assert not served_sent_model.is_ready()

    served_sent_model.load()

    assert served_sent_model.is_ready()


@pytest.mark.parametrize("test_record_index", [0, 1, 2])
def test_served_sent_model_predict(
    test_served_model_artifacts,
    test_inputs,
    test_predictions,
    test_record_index,
    test_atol,
    test_rtol,
):
    """Tests the fully initialized and loaded ServedSentModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_sent_model = ServedSentModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_sent_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(language="en"),
        inputs=PredictInputContentModel(content=test_inputs[test_record_index]),
    )

    actual_output = served_sent_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            label=test_predictions[test_record_index].get("label"),
            negative_prob=test_predictions[test_record_index].get("negative_prob"),
            positive_prob=test_predictions[test_record_index].get("positive_prob"),
            entities=test_predictions[test_record_index].get("entities"),
        )
    )

    assert actual_output.outputs.label == expected_output.outputs.label
    torch.testing.assert_close(
        actual_output.outputs.positive_prob,
        expected_output.outputs.positive_prob,
        atol=test_atol,
        rtol=test_rtol,
    )
    torch.testing.assert_close(
        actual_output.outputs.negative_prob,
        expected_output.outputs.negative_prob,
        atol=test_atol,
        rtol=test_rtol,
    )


@pytest.mark.parametrize(
    "test_sample_content, test_sample_entities, test_sample_response",
    [
        (
            "I love John. I hate Jack",
            [{"text": "John"}, {"text": "Jack"}],
            {
                "label": "negative",
                "negative_prob": 0.4735,
                "positive_prob": 0.4508,
                "entities": [
                    {"text": "John", "sentiment": "positive"},
                    {"text": "Jack", "sentiment": "negative"},
                ],
            },
        )
    ],
)
def test_served_sent_model_with_entities_predict(
    test_served_model_artifacts,
    test_sample_content,
    test_sample_entities,
    test_sample_response,
):
    """Tests the fully initialized and loaded ServedSentModel's predict method, using the
    custom data models for validation and the test files from the model artifact as ground truth
    for the regression test element."""

    served_sent_model = ServedSentModel(
        served_model_artifacts=test_served_model_artifacts
    )
    served_sent_model.load()
    input = PredictRequestModel(
        configuration=PredictConfiguration(
            language="en", entities=test_sample_entities
        ),
        inputs=PredictInputContentModel(content=test_sample_content),
    )

    actual_output = served_sent_model.predict(input)

    expected_output = PredictResponseModel(
        outputs=PredictionOutputContent(
            label=test_sample_response.get("label"),
            negative_prob=test_sample_response.get("negative_prob"),
            positive_prob=test_sample_response.get("positive_prob"),
            entities=test_sample_response.get("entities"),
        )
    )

    assert (
        actual_output.outputs.entities[0].text
        == expected_output.outputs.entities[0].text
    )
    assert (
        actual_output.outputs.entities[0].sentiment
        == expected_output.outputs.entities[0].sentiment
    )


@pytest.mark.order(3)
def test_served_sent_model_bio(
    test_model_name, test_served_model_artifacts, test_model_card
):
    """Tests the fully initialized and loaded ServedSentModel's bio method, using the
    custom data models for validation and the model card from the model artifact as ground truth
    for the regression test element."""

    served_sent_model = ServedSentModel(
        served_model_artifacts=test_served_model_artifacts
    )

    served_sent_model.load()

    actual_output = served_sent_model.bio()
    expected_output = BioResponseModel(
        model_name=test_model_name, model_card=test_model_card
    )

    assert actual_output == expected_output
