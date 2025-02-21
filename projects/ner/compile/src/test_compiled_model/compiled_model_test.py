"""Compiled model tests."""

# Standard Library
import json
from typing import List

# 3rd party libraries
import numpy as np
import pandas as pd
import pytest
from conftest import parametrize_values

# Internal libraries
from onclusiveml.compile.constants import CompileWorkflowTasks


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


@pytest.mark.parametrize("test_sample_index, language, lang_index", parametrize_values)
def test_compiled_model_regression(  # type: ignore[no-untyped-def]
    logger,
    settings,
    compiled_ner,
    test_files,
    test_files_predictions,
    test_sample_index,
    language,
    lang_index,
    compilation_test_settings,
):
    """Perform regression testing for the compiled NER model.

    Args:
        logger: Logger instance for logging
        settings: IO settigns for workflow component
        compiled_ner: Compiled NER model instance
        test_files: Dictionary containing test input
        test_files_predictions: List of expected predictions for test sample
        test_sample_index (int): Index of the test sample being processed.
        language (str): Language of the sample text.
        lang_index (int): Index of sample texts where each list is specific language
        compilation_test_settings: Compilation settings
    """
    compiled_predictions = compiled_ner(
        [test_files["inputs"][lang_index][test_sample_index]], language=language
    )
    # Converting from pydantic classes to dictionaries to allow conversion to
    # dictionary more simpler
    compiled_predictions_dict = [obj._asdict() for obj in compiled_predictions[0]]
    # Create copies of the lists of dictionaries
    compiled_predictions_list_copy = [dict(d) for d in compiled_predictions_dict]
    test_sample_list = [
        dict(d) for d in test_files_predictions[lang_index][test_sample_index]
    ]
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
    # ensure score columns are matching float types
    compiled_predictions_df["score"] = compiled_predictions_df["score"].astype(
        "float32"
    )
    expected_predictions_df["score"] = expected_predictions_df["score"].astype(
        "float32"
    )
    # assert ner are identical and scores are within 0.01 absolute deviation
    pd.testing.assert_frame_equal(
        compiled_predictions_df,
        expected_predictions_df,
        rtol=compilation_test_settings.regression_rtol,
        atol=compilation_test_settings.regression_atol,
    )

    def json_serializable(obj):
        if isinstance(obj, (np.float32, np.float64)):
            return float(obj)

    # create new export file or append prediction to existing exported prediction file
    try:
        with open(
            settings.test_files(CompileWorkflowTasks.TEST)["predictions"],
            "r",
            encoding="utf-8",
        ) as compiled_predictions_file:
            all_compiled_predictions = json.load(compiled_predictions_file)
    except (FileExistsError, FileNotFoundError, json.JSONDecodeError):
        all_compiled_predictions = [[], []]

    all_compiled_predictions[lang_index].append(compiled_predictions_dict)

    with open(
        settings.test_files(CompileWorkflowTasks.TEST)["predictions"],
        "w",
        encoding="utf-8",
    ) as compiled_predictions_file:
        json.dump(
            all_compiled_predictions,
            compiled_predictions_file,
            default=json_serializable,
        )
