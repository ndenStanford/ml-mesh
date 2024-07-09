"""Compiled model test."""

# Standard Library
import json

# ML libs
import torch

# Internal libraries
from onclusiveml.models.iptc.compiled_iptc import extract_model_id

# Source
from src.settings import (
    UncompiledTrackedModelSettings,  # type: ignore[attr-defined]
)


def test_compiled_model_regression(  # type: ignore[no-untyped-def]
    io_settings,
    compiled_iptc,
    test_files,
    compilation_test_settings,
    class_dict,
    id_to_topic,
):
    """Perform regression testing for the compiled iptc model.

    Args:
        io_settings: IO settigns for workflow component
        compiled_iptc: Compiled IPTC model instance
        test_files: Dictionary containing test input
        compilation_test_settings: Compilation settings
        class_dict: Dictionary containing class name
        id_to_topic: model_id to class name
    """
    assert len(test_files["inputs"]) == len(test_files["predictions"]["labels"])
    total_sample_size = len(test_files["inputs"])
    model_specs = UncompiledTrackedModelSettings()
    model_id = extract_model_id(model_specs.project)
    class_dict_dict = class_dict[id_to_topic[model_id]]
    for test_sample_index in range(total_sample_size):

        compiled_pred = compiled_iptc(test_files["inputs"][test_sample_index])
        compiled_predictions = [iptc.model_dump() for iptc in compiled_pred][0]
        expected_predictions_prob = test_files["predictions"]["probs"][
            test_sample_index
        ]
        logits_tensor = torch.tensor(expected_predictions_prob)
        probabilities = torch.softmax(logits_tensor, dim=0)
        max_prob, max_index = torch.max(probabilities, dim=0)
        torch.testing.assert_close(
            compiled_predictions["score"],
            max_prob.item(),
            atol=compilation_test_settings.regression_atol,
            rtol=compilation_test_settings.regression_rtol,
        )
        assert compiled_predictions["label"] == class_dict_dict[max_index.item()]
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
    model_specs = UncompiledTrackedModelSettings()
    model_id = extract_model_id(model_specs.project)
    test_sample_content, test_sample_response = test_samples[model_id]
    compiled_pred = compiled_iptc(test_sample_content)
    compiled_predictions = [iptc.model_dump() for iptc in compiled_pred][0]
    assert compiled_predictions["label"] == test_sample_response["label"]
