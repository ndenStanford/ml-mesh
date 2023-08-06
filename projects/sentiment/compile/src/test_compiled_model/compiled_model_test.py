# Standard Library
import json
from typing import List

# ML libs
import torch

# 3rd party libraries
import pandas as pd


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


def compiled_model_regression_test(  # type: ignore[no-untyped-def]
    io_settings, compiled_sent, test_files, regression_test_atol, regression_test_rtol
):

    assert len(test_files["inputs"]) == len(test_files["predictions"])
    total_sample_size = len(test_files["inputs"])

    for test_sample_index in range(total_sample_size):

        compiled_predictions = compiled_sent.extract_sentiment(
            test_files["inputs"][test_sample_index]
        )

        expected_predictions = test_files["predictions"][test_sample_index]

        if expected_predictions["label"] == "positive":
            compiled_predictions_score = compiled_predictions["positive_prob"]
        elif expected_predictions["label"] == "negative":
            compiled_predictions_score = compiled_predictions["negative_prob"]
        else:
            compiled_predictions_score = (
                1
                - compiled_predictions["positive_prob"]
                - compiled_predictions["negative_prob"]
            )

        torch.testing.assert_close(
            compiled_predictions_score,
            expected_predictions["score"],
            atol=regression_test_atol,
            rtol=regression_test_rtol,
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
