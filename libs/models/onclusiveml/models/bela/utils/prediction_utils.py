# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Standard Library
from collections import defaultdict
from functools import lru_cache

# Internal libraries
from onclusiveml.models.bela.transforms.spm_transform import SPMTransform


@lru_cache
def get_sp_transform():
    return SPMTransform(max_seq_len=100000)


def get_windows(text, window_length=254, overlap=127):
    sp_transform = get_sp_transform()
    tokens = sp_transform([text])[0]
    tokens = tokens[1:-1]
    windows = []
    for window_start in range(0, len(tokens), window_length - overlap):
        start_pos = tokens[window_start][1]
        if window_start + window_length >= len(tokens):
            end_pos = tokens[-1][2]
        else:
            end_pos = tokens[window_start + window_length][2]
        windows.append((start_pos, end_pos))
    return windows


def convert_predictions_to_dict(example_predictions):
    if len(example_predictions) > 0:
        offsets, lengths, entities, md_scores, el_scores = zip(*example_predictions)
    else:
        offsets, lengths, entities, md_scores, el_scores = [], [], [], [], []
    return {
        "offsets": offsets,
        "lengths": lengths,
        "entities": entities,
        "md_scores": md_scores,
        "el_scores": el_scores,
    }


def group_predictions_by_example(all_predictions, extended_examples):
    grouped_predictions = defaultdict(list)
    for prediction, extended_example in zip(all_predictions, extended_examples):
        window_start = extended_example["window_start"]
        prediction = dict(prediction)
        prediction["offsets"] = [
            offset + window_start for offset in prediction["offsets"]
        ]
        grouped_predictions[extended_example["document_id"]].append((prediction))

    predictions = {}
    for document_id, example_prediction_list in grouped_predictions.items():
        example_predictions = []
        for prediction in example_prediction_list:
            for offset, length, ent, md_score, el_score in zip(
                prediction["offsets"],
                prediction["lengths"],
                prediction["entities"],
                prediction["md_scores"],
                prediction["el_scores"],
            ):
                example_predictions.append((offset, length, ent, md_score, el_score))
                example_predictions = sorted(example_predictions)
        predictions[document_id] = example_predictions

    return predictions


def merge_predictions(example_predictions):
    filtered_example_predictions = []

    current_end = None
    current_offset = None
    current_length = None
    current_ent_id = None
    current_md_score = None
    current_el_score = None

    for offset, length, ent_id, md_score, el_score in example_predictions:
        if current_end is None:
            current_end = offset + length
            current_offset = offset
            current_length = length
            current_ent_id = ent_id
            current_md_score = md_score
            current_el_score = el_score
            continue

        if offset < current_end:
            # intersection of two predictions
            if md_score > current_md_score:
                current_ent_id = ent_id
                current_offset = offset
                current_length = length
                current_md_score = md_score
                current_el_score = el_score
        else:
            filtered_example_predictions.append(
                (
                    current_offset,
                    current_length,
                    current_ent_id,
                    current_md_score,
                    current_el_score,
                )
            )
            current_ent_id = ent_id
            current_offset = offset
            current_length = length
            current_md_score = md_score
            current_el_score = el_score

        current_end = offset + length

    if current_offset is not None:
        filtered_example_predictions.append(
            (
                current_offset,
                current_length,
                current_ent_id,
                current_md_score,
                current_el_score,
            )
        )

    return filtered_example_predictions
