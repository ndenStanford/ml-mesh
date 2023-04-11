import pytest
from pydantic import List

@pytest.fixture
def huggingface_model_references() -> List[str]:
    
    return (
        'prajjwal1/bert-tiny'
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
    )
    
@pytest.fixture
def huggingface_pipeline_tasks() -> List[str]:
    
    return [
        'feature-extraction',
        'text-classification'
    ]