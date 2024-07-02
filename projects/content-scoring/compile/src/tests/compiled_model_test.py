"""Compiled model tests."""


def test_compiled_model_regression(
    test_files_inputs,
    test_files_predictions,
):
    """Dummy model for compile component.

    Args:
        test_files_predictions: List of expected predictions for test sample
        test_files_inputs (int): Index of the test sample being processed.
    """
    assert test_files_inputs != test_files_predictions
