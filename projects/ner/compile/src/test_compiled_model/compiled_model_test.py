# Standard Library
import json
from typing import List

# 3rd party libraries
import pandas as pd
import pytest


def to_dataframe(extract_entites: List[dict]) -> pd.DataFrame:

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


"""
NOTE: handler makes changes to the output by merging inner and outer tags
into one tag and so modify expected predictions here
"""


@pytest.mark.parametrize("test_sample_index", [0, 1, 2, 3])
def compiled_model_regression_test(  # type: ignore[no-untyped-def]
    logger,
    io_settings,
    compiled_ner,
    test_files,
    test_files_predictions,
    test_sample_index,
    compilation_test_settings,
):
    compiled_predictions = compiled_ner.extract_entities(
        test_files["inputs"][test_sample_index], language="en", return_pos=True
    )

    assert compiled_predictions == test_files_predictions[test_sample_index]
    # Converting from pydantic classes to dictionaries to allow conversion to
    # dictionary more simpler
    compiled_predictions_dict = [obj.__dict__ for obj in compiled_predictions]

    compiled_predictions_df = to_dataframe(compiled_predictions_dict)
    expected_predictions_df = to_dataframe(test_files_predictions[test_sample_index])
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
