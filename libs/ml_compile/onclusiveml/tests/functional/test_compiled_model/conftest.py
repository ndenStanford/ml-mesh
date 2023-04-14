# Standard Library
from typing import List

# ML libs
from transformers import AutoModel, AutoTokenizer

# 3rd party libraries
import pytest


@pytest.fixture
def huggingface_tokenizer(huggingface_model_reference: str):

    return AutoTokenizer.from_pretrained(huggingface_model_reference)


@pytest.fixture
def huggingface_model(huggingface_model_reference: str):

    return AutoModel.from_pretrained(huggingface_model_reference)


@pytest.fixture
def huggingface_model_max_length(huggingface_tokenizer):

    return huggingface_tokenizer.model_max_length


@pytest.fixture
def sample_inputs() -> List[str]:

    return (
        [
            "This is a short sample input.",
            """This is another sample input. This is to test how the compiled model handles more
            than one tokenized sample at a time.""",
        ]
        * 3  # noqa: W503
    )


@pytest.fixture
def regression_test_atol():
    return 2e-02


@pytest.fixture
def regression_test_rtol():
    return 1e-02
