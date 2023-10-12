"""Compiled model test."""

# Standard Library
import json

# ML libs
import torch

# 3rd party libraries
import pytest


def test_compiled_model_regression(  # type: ignore[no-untyped-def]
    io_settings, compiled_iptc, test_files, compilation_test_settings
):
    """Perform regression testing for the compiled iptc model.

    Args:
        io_settings: IO settigns for workflow component
        compiled_iptc: Compiled IPTC model instance
        test_files: Dictionary containing test input
        compilation_test_settings: Compilation settings
    """
    assert len(test_files["inputs"]) == len(test_files["predictions"])
    total_sample_size = len(test_files["inputs"])

    for test_sample_index in range(total_sample_size):

        compiled_predictions = compiled_iptc.extract_iptc(
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
            atol=compilation_test_settings.regression_atol,
            rtol=compilation_test_settings.regression_rtol,
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
                    {"text": "John", "iptc": "positive"},
                    {"text": "Jack", "iptc": "negative"},
                ],
            },
        )
    ],
)
def compiled_model_entity_iptc_test(  # type: ignore[no-untyped-def]
    compiled_iptc, test_sample_content, test_sample_entities, test_sample_response
):
    """Perform iptc testing with entities input for the compiled iptc model.

    Args:
        compiled_iptc: Compiled IPTC model instance
        test_sample_content (str): Sample content to be tested
        test_sample_entities (str): Sample entities to be tested
        test_sample_response (str): Sample response to be compared with
    """
    compiled_predictions = compiled_iptc.extract_iptc(
        test_sample_content, test_sample_entities
    )

    assert (compiled_predictions["entities"].sort(key=lambda x: x["text"])) == (
        test_sample_response["entities"].sort(key=lambda x: x["text"])
    )
