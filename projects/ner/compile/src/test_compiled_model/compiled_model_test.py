"""Compiled model tests."""

# Standard Library
import json
from typing import List

# 3rd party libraries
import pandas as pd
import pytest


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


@pytest.mark.order(1)
@pytest.mark.parametrize(
    "test_sample_index, language, lang_index",
    [
        ([0, 1, 2, 3], "en", 0),
        ([0, 1, 2, 3], "ja", 1),
    ],
)
def test_compiled_model_regression(  # type: ignore[no-untyped-def]
    logger,
    io_settings,
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
        io_settings: IO settigns for workflow component
        compiled_ner: Compiled NER model instance
        test_files: Dictionary containing test input
        test_files_predictions: List of expected predictions for test sample
        test_sample_index (int): Index of the test sample being processed.
        language (str): Specfiy the language of the sample text
        lang_index (int): Specify the location of sample texts for given language
        compilation_test_settings: Compilation settings
    """
    for i in test_sample_index:
        compiled_predictions = compiled_ner.extract_entities(
            test_files["inputs"][lang_index][i], language=language, return_pos=True
        )

        assert compiled_predictions == test_files_predictions[lang_index][i]
        # Converting from pydantic classes to dictionaries to allow conversion to
        # dictionary more simpler
        compiled_predictions_dict = [obj.__dict__ for obj in compiled_predictions]

        compiled_predictions_df = to_dataframe(compiled_predictions_dict)
        expected_predictions_df = to_dataframe(test_files_predictions[lang_index][i])
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
