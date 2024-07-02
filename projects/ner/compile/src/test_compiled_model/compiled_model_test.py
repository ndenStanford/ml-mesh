"""Compiled model tests."""

# Standard Library
import json
from typing import List

# 3rd party libraries
import pandas as pd

# Source
from src.settings import (
    UncompiledTrackedModelSpecs,  # type: ignore[attr-defined]
)


def to_dataframe(extract_entites: List[dict]) -> pd.DataFrame:
    """Convert a list of extracted entities into a dataframe.

    Args:
        extract_entities (List[dict]): List of dictionaries representing entities

    Returns:
        pd.DataFrame: Dataframe containing extracted enitities with specified columns
    """
    df = pd.DataFrame(
        extract_entites,
        columns=[
            "entity_type",
            "entity_text",
            "score",
            "sentence_index",
            "start",
            "end",
        ],
    )
    df_sorted = df.sort_values(by="sentence_index", ascending=True).reset_index(
        drop=True
    )

    return df_sorted


def test_compiled_model_regression(  # type: ignore[no-untyped-def]
    logger,
    io_settings,
    compiled_ner,
    test_files,
    test_files_predictions,
    compilation_test_settings,
):
    """Perform regression testing for the compiled NER model.

    Args:
        logger: Logger instance for logging
        io_settings: IO settigns for workflow component
        compiled_ner: Compiled NER model instance
        test_files: Dictionary containing test input
        test_files_predictions: List of expected predictions for test sample
        compilation_test_settings: Compilation settings
    """
    # modified logic that tests only 1 sample given the model either English or multilingual
    model_specs = UncompiledTrackedModelSpecs()
    project = model_specs.project
    language = compilation_test_settings.language
    compiled_predictions = compiled_ner([test_files["inputs"]], language=language)
    # Converting from pydantic classes to dictionaries to allow conversion to
    # dictionary more simpler
    compiled_predictions_dict = [obj._asdict() for obj in compiled_predictions[0]]

    # Create copies of the lists of dictionaries
    compiled_predictions_list_copy = [dict(d) for d in compiled_predictions_dict]
    test_sample_list = [dict(d) for d in test_files_predictions[project]]
    test_sample_list_copy = [dict(d) for d in test_sample_list]

    # Function to remove '##' from entity_text
    def clean_entity_text(d):
        if "entity_text" in d:
            d["entity_text"] = d["entity_text"].replace("##", "")

    # Apply the function to each dictionary in both lists
    for d in compiled_predictions_dict:
        clean_entity_text(d)

    for d in compiled_predictions_list_copy:
        d.pop("score", None)
        clean_entity_text(d)

    for d in test_sample_list_copy:
        d.pop("score", None)

    # Now assert the equality of the modified lists of dictionaries
    assert compiled_predictions_list_copy == test_sample_list_copy

    compiled_predictions_df = to_dataframe(compiled_predictions_dict)
    expected_predictions_df = to_dataframe(test_sample_list)

    # assert ner are identical and scores are within 0.01 absolute deviation
    pd.testing.assert_frame_equal(
        compiled_predictions_df,
        expected_predictions_df,
        rtol=compilation_test_settings.regression_rtol,
        atol=compilation_test_settings.regression_atol,
    )
    # create new export file or append prediction to existing exported prediction file
    try:
        with open(
            io_settings.test.test_files["predictions"]
        ) as compiled_predictions_file:
            all_compiled_predictions = json.load(compiled_predictions_file)
    except (FileExistsError, FileNotFoundError):
        all_compiled_predictions = []

    all_compiled_predictions.append(compiled_predictions_dict)

    with open(
        io_settings.test.test_files["predictions"], "w"
    ) as compiled_predictions_file:
        json.dump(all_compiled_predictions, compiled_predictions_file)
