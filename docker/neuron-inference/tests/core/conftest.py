# Standard Library
import os
from typing import List, Tuple

# ML libs
import torch
from transformers import AutoTokenizer

# 3rd party libraries
import pytest


@pytest.fixture()
def test_output_dir() -> str:

    return os.path.join(".", "test", "output")


@pytest.fixture()
def torch_function_input() -> Tuple[torch.Tensor, torch.Tensor]:

    return (torch.rand(3), torch.rand(3))


@pytest.fixture()
def torch_graph_input() -> torch.Tensor:

    return torch.rand(1, 1, 3, 3)


@pytest.fixture
def torch_model_text_input() -> List[str]:

    return [
        "This is a sentence record to generate sample inputs for the neuron compilation step",
        "This is the second record to generate tracing compilation inputs.",
        "This is the third text record. It has more than one sentence.",
    ]


@pytest.fixture
def torch_model_name() -> str:
    return "prajjwal1/bert-tiny"


@pytest.fixture
def torch_model_input(torch_model_name, torch_model_text_input) -> torch.Tensor:

    tokenizer = AutoTokenizer.from_pretrained(torch_model_name)

    tokens = tokenizer(
        torch_model_text_input,
        add_special_tokens=True,
        padding="max_length",
        max_length=50,
        truncation=True,
        return_tensors="pt",
    )

    return tokens["input_ids"], tokens["attention_mask"]
