# Standard Library
import json
from typing import List, Tuple

# 3rd party libraries
import pandas as pd
import pytest


def to_dataframe(extracted_keywords: List[Tuple[str, float]]) -> pd.DataFrame:

    return pd.DataFrame(extracted_keywords, columns=["keyword", "score"])


@pytest.mark.order(1)
@pytest.mark.parametrize("test_sample_index", [0, 1, 2])
def compiled_model_regression_test(
    logger,
    io_settings,
    compiled_keybert,
    test_files,
    test_sample_index,
    compilation_test_settings,
):

    compiled_predictions = compiled_keybert.extract_keywords(
        test_files["inputs"][test_sample_index], **test_files["inference_params"]
    )
    # regression test compiled vs uncompiled
    expected_predictions = test_files["predictions"][test_sample_index]

    logger.info(
        f"Compiled model predictions {test_sample_index} : {compiled_predictions}"
    )
    logger.info(
        f"Expected model predictions {test_sample_index}: {expected_predictions}"
    )

    compiled_predictions_df = to_dataframe(compiled_predictions)
    expected_predictions_df = to_dataframe(expected_predictions)
    # assert keywords are identical and scores are within 0.01 absolute deviation
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
