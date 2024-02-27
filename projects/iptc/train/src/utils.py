"""Utility functions."""
# 3rd party libraries
from class_dict import CLASS_DICT
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


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
        return len(CLASS_DICT)
    elif level == 2:
        return len(CLASS_DICT[first_level_root])
    elif level == 3:
        return len(CLASS_DICT[first_level_root][second_level_root])
