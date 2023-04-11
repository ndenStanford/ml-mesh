import pytest
from typing import List
from transformers import AutoTokenizer, AutoModel

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
def sample_inputs(batch_size) -> List[str]:
    
    return [
        'This is a sample input. it has more thant 10 tokens to tokenize.',
        'This is another sample input. This is to test how the compiled model handles more than one tokenized sample at a time.'
    ][:batch_size]
    
@pytest.fixture
def regression_test_atol():
    return 2e-02

@pytest.fixture
def regression_test_rtol():
    return 1e-02