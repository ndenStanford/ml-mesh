import pytest
from typing import List
from transformers.pipelines import pipeline

@pytest.fixture
def huggingface_pipeline(huggingface_pipeline_task: str, huggingface_model_reference: str):
    
    return pipeline(task=huggingface_pipeline_task, model=huggingface_model_reference)

@pytest.fixture
def custom_tokenization_settings(max_length: int):
    
    return {'padding':'max_length', 'truncation': True, 'add_special_tokens': True, 'max_length': max_length}

@pytest.fixture
def sample_inputs() -> List[str]:
    
    return [
        'This is an extremely bad and short sample input.',
        'This is a pretty neutral sentence.'
        'This is another, much, much better sample input. It is amazing! This is to test how the compiled model handles more than one tokenized sample at a time.'
    ] * 2
    
@pytest.fixture
def regression_test_atol():
    return 2e-02

@pytest.fixture
def regression_test_rtol():
    return 1e-02