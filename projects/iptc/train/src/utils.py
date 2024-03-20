"""Utility functions."""

# Standard Library
import re

# 3rd party libraries
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Source
from src.class_dict import CLASS_DICT_FIRST, CLASS_DICT_SECOND, CLASS_DICT_THIRD


def compute_metrics(pred):  # type: ignore[no-untyped-def]
    """Compute metrics function for binary classification."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="weighted"
    )
    acc = accuracy_score(labels, preds)
    return {"accuracy": acc, "f1": f1, "precision": precision, "recall": recall}


def find_num_labels(  # type: ignore[no-untyped-def]
    level, first_level_root=None, second_level_root=None
):
    """Retrieve the number of labels from the CLASS_DICT file."""
    if level == 1:
        return len(CLASS_DICT_FIRST["root"])
    elif level == 2:
        return len(CLASS_DICT_SECOND[first_level_root])
    elif level == 3:
        return len(CLASS_DICT_THIRD[first_level_root][second_level_root])


def extract_model_id(project: str) -> str:
    """Extracts the model ID from a project string.

    Args:
        project (str): The project string, e.g., 'onclusive/iptc-00000000'.

    Returns:
        str: The extracted model ID.

    Raises:
        ValueError: If the model ID cannot be found in the project string.
    """
    match = re.search(r"onclusive/iptc-(.+)", project)
    if match:
        return match.group(1)  # Return the matched group, which is the model ID
    else:
        raise ValueError(f"Model ID not found in project string: '{project}'")


def find_category_for_subcategory(  # type: ignore[no-untyped-def]
    class_dict, target_subcategory
):
    """Function to find the top-level category for a given sub-category."""
    for top_category, subcategories in class_dict.items():
        if target_subcategory in subcategories.values():
            return top_category


def topic_conversion(df):  # type: ignore[no-untyped-def]
    """Update the topic name to fix the discrepencies between class_dict and training data."""
    df["topic_1"] = df["topic_1"].replace(
        ["arts, culture and entertainment"], "arts, culture, entertainment and media"
    )
    df["topic_1"] = df["topic_1"].replace(
        ["conflicts, war and peace"], "conflict, war and peace"
    )
    return df
