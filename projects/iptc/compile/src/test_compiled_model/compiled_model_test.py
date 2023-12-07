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

        compiled_pred = compiled_iptc(test_files["inputs"][test_sample_index])
        compiled_predictions = [iptc.dict() for iptc in compiled_pred][0]
        expected_predictions = test_files["predictions"][test_sample_index]

        torch.testing.assert_close(
            compiled_predictions["score"],
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
    "test_sample_content, test_sample_response",
    [
        (
            """Stocks reversed earlier losses to close higher despite rising oil prices
            that followed the attack by Hamas on Israel over the weekend. Dovish comments by
            Federal Reserve officials boosted the three major indexes. The Dow Jones Industrial
            Average added nearly 200 points.""",
            {"label": "economy, business and finance", "score": 0.9870237112045288},
        )
    ],
)
def compiled_model_entity_iptc_test(  # type: ignore[no-untyped-def]
    compiled_iptc, test_sample_content, test_sample_response
):
    """Perform iptc label testing with input for the compiled iptc model.

    Args:
        compiled_iptc: Compiled IPTC model instance
        test_sample_content (str): Sample content to be tested
        test_sample_response (str): Sample response to be compared with
    """
    compiled_pred = compiled_iptc(test_sample_content)
    compiled_predictions = [iptc.dict() for iptc in compiled_pred][0]
    assert (compiled_predictions["label"]) == (test_sample_response["label"])
