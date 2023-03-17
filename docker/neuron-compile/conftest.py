import pytest
import torch
from typing import List


@pytest.fixture
def image_tracing_input() -> torch.Tensor:

    return torch.rand([1, 3, 224, 224])


@pytest.fixture
def text_tracing_input() -> List[str]:

    return [
        "This is a sentence record to generate sample inputs for the neuron compilation step",
        "This is the second record to generate tracing compilation inputs.",
        "This is the third text record. It has more than one sentence.",
    ]


@pytest.fixture
def max_length() -> int:

    return 25