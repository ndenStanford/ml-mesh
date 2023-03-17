import pytest
import torch


@pytest.fixture
def image_tracing_input():
    
    return torch.rand([1, 3, 224, 224])

@pytest.fixture
def text_tracing_input():
    
    return "This is a sentence sentence to generate sample inputs for the neuron compilation step"