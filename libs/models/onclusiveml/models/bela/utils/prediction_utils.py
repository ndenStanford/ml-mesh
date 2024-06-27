"""Utils."""

# Standard Library
from collections import defaultdict
from functools import lru_cache

# Internal libraries
from onclusiveml.models.bela.transforms.spm_transform import SPMTransform


@lru_cache
def get_sp_transform():
    """SPM transform."""
    return SPMTransform(max_seq_len=100000)


def get_windows(text, window_length=254, overlap=127):
    """Extracts windows of text based on token boundaries.

    This function divides the input text into overlapping windows of a specified
    length, based on token boundaries obtained from a SentencePiece (SP) tokenizer.

    Args:
        text (str): The input text to be divided into windows.
        window_length (int, optional): The desired length of each window. Default is 254.
        overlap (int, optional): The amount of overlap between consecutive windows. Default is 127.

    Returns:
        list: A list of tuples representing the start and end positions of each window
              within the original text, based on token boundaries.
    """
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
    """Convert predictions into a dict."""
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
    """Groups predictions by example and adjusts offsets.

    This function groups predictions based on their associated extended examples
    and adjusts offsets relative to the original document start position.

    Args:
        all_predictions (list): A list of predictions, where each prediction is a dictionary
                                containing keys like "offsets", "lengths", "entities",
                                "md_scores", and "el_scores".
        extended_examples (list): A list of extended examples, where each example is a dictionary
                                  containing keys like "window_start", "document_id", and others
                                  needed to associate predictions with their original documents.

    Returns:
        dict: A dictionary where keys are document IDs and values are lists of predictions
              adjusted for offsets relative to the document start. Each prediction is a tuple
              containing (offset, length, entity, md_score, el_score).
    """
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
    """Merges overlapping predictions and filters redundant predictions.

    This function takes a list of predictions and merges overlapping predictions
    based on their offsets. It also filters redundant predictions by keeping the
    prediction with the highest confidence score (md_score).

    Args:
        example_predictions (list): A list of predictions, where each prediction is a tuple
                                    containing (offset, length, ent_id, md_score, el_score).

    Returns:
        list: A filtered list of merged predictions, where each prediction tuple contains
              (offset, length, ent_id, md_score, el_score).
    """
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
