# Standard Library
import json

# ML libs
import torch

# 3rd party libraries
import pytest


def compiled_model_regression_test(  # type: ignore[no-untyped-def]
    io_settings, compiled_sent, test_files, test_atol, test_rtol
):

    assert len(test_files["inputs"]) == len(test_files["predictions"])
    total_sample_size = len(test_files["inputs"])

    for test_sample_index in range(total_sample_size):

        compiled_predictions = compiled_sent.extract_sentiment(
            test_files["inputs"][test_sample_index]
        )

        expected_predictions = test_files["predictions"][test_sample_index]

        if expected_predictions["label"] == "positive":
            compiled_predictions_score = compiled_predictions["positive_prob"]
        elif expected_predictions["label"] == "negative":
            compiled_predictions_score = compiled_predictions["negative_prob"]
        else:
            compiled_predictions_score = (
                1
                - compiled_predictions["positive_prob"]
                - compiled_predictions["negative_prob"]
            )

        torch.testing.assert_close(
            compiled_predictions_score,
            expected_predictions["score"],
            atol=test_atol,
            rtol=test_rtol,
        )
        # create new export file or append prediction to existing exported prediction file
        try:
            with open(
                io_settings.test.test_files["predictions"]
            ) as compiled_predictions_file:
                all_compiled_predictions = json.load(compiled_predictions_file)
        except (FileExistsError, FileNotFoundError):
            all_compiled_predictions = []

        all_compiled_predictions.append(compiled_predictions)

        with open(
            io_settings.test.test_files["predictions"], "w"
        ) as compiled_predictions_file:
            json.dump(all_compiled_predictions, compiled_predictions_file)


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
def compiled_model_entity_sentiment_test(  # type: ignore[no-untyped-def]
    compiled_sent, test_sample_content, test_sample_entities, test_sample_response
):

    compiled_predictions = compiled_sent.extract_sentiment(
        test_sample_content, test_sample_entities
    )

    assert (compiled_predictions["entities"].sort(key=lambda x: x["text"])) == (
        test_sample_response["entities"].sort(key=lambda x: x["text"])
    )
