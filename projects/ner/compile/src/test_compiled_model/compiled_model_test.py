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


@pytest.mark.parametrize(
    "test_sample_index, expected_predictions",
    [
        (
            0,
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Google",
                    "score": "0.9981779",
                    "sentence_index": 0,
                    "start": 0,
                    "end": 6,
                },
                {
                    "entity_type": "LOC",
                    "entity_text": "Mountain View",
                    "score": "0.99910104",
                    "sentence_index": 0,
                    "start": 16,
                    "end": 29,
                },
                {
                    "entity_type": "LOC",
                    "entity_text": "CA",
                    "score": "0.99936694",
                    "sentence_index": 0,
                    "start": 31,
                    "end": 33,
                },
            ],
        ),
        (
            1,
            [
                {
                    "entity_type": "LOC",
                    "entity_text": "Gulf Stream",
                    "score": "0.9890644",
                    "sentence_index": 0,
                    "start": 21,
                    "end": 32,
                },
                {
                    "entity_type": "LOC",
                    "entity_text": "Cape Cod",
                    "score": "0.9871611",
                    "sentence_index": 0,
                    "start": 81,
                    "end": 89,
                },
            ],
        ),
        (
            2,
            [
                {
                    "entity_type": "LOC",
                    "entity_text": "Jupiter",
                    "score": "0.99254674",
                    "sentence_index": 0,
                    "start": 105,
                    "end": 112,
                }
            ],
        ),
        (
            3,
            [
                {
                    "entity_type": "ORG",
                    "entity_text": "Loggerhead",
                    "score": "0.62161815",
                    "sentence_index": 0,
                    "start": 10,
                    "end": 20,
                },
                {
                    "entity_type": "LOC",
                    "entity_text": "Marinelife Center",
                    "score": "0.8719994",
                    "sentence_index": 0,
                    "start": 21,
                    "end": 38,
                },
            ],
        ),
    ],
)
def compiled_model_regression_test(  # type: ignore[no-untyped-def]
    logger,
    io_settings,
    compiled_ner,
    test_files,
    test_sample_index,
    expected_predictions,
    compilation_test_settings,
):
    compiled_predictions = compiled_ner.extract_entities(
        test_files["inputs"][test_sample_index], **test_files["inference_params"]
    )

    assert compiled_predictions == expected_predictions
    compiled_predictions_df = to_dataframe(compiled_predictions)
    expected_predictions_df = to_dataframe(expected_predictions)
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

    all_compiled_predictions.append(compiled_predictions)

    with open(
        io_settings.test.test_files["predictions"], "w"
    ) as compiled_predictions_file:
        json.dump(all_compiled_predictions, compiled_predictions_file)
