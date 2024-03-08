"""Compiled model test."""

# Standard Library
import json

# ML libs
import torch

# Internal libraries
from onclusiveml.models.iptc.compiled_iptc import extract_model_id

# Source
from src.settings import (
    UncompiledTrackedModelSpecs,  # type: ignore[attr-defined]
)


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


def compiled_model_entity_iptc_test(  # type: ignore[no-untyped-def]
    compiled_iptc, test_samples
):
    """Perform iptc label testing with input for the compiled iptc model.

    Args:
        compiled_iptc: Compiled IPTC model instance
        test_samples (dict): A dictionary where each key is a unique identifier for a test sample,
                            and each value is a tuple containing the sample content to be tested
                            and the expected sample response.
    """
    model_specs = UncompiledTrackedModelSpecs()
    model_id = extract_model_id(model_specs.project)
    test_sample_content, test_sample_response = test_samples[model_id]
    compiled_pred = compiled_iptc(test_sample_content)
    compiled_predictions = [iptc.dict() for iptc in compiled_pred][0]
    assert compiled_predictions["label"] == test_sample_response["label"]
