# 3rd party libraries
import numpy as np
import pytest
from datasets import Dataset


@pytest.fixture(scope="session")
def test_train_dataset():
    seq_len, dataset_size = 512, 512
    dummy_data = {
        "input_ids": np.random.randint(100, 30000, (dataset_size, seq_len)),
        "labels": np.random.randint(0, 1, (dataset_size)),
    }
    ds = Dataset.from_dict(dummy_data)
    ds.set_format("pt")

    return ds


@pytest.fixture
def test_model_reference():

    return "distilbert-base-uncased"


@pytest.fixture
def test_default_training_params():

    return {
        "output_dir": "tmp",
        "evaluation_strategy": "steps",
        "num_train_epochs": 1,
        "optim": "adafactor",
        "log_level": "error",
        "report_to": "none",
    }
