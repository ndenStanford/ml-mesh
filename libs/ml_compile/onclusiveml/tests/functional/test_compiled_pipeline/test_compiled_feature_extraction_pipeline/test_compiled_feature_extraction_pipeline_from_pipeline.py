import pytest
from onclusiveml.ml_compile import CompiledPipeline
from typing import List, Tuple
import numpy as np


@pytest.mark.parametrize(
    'huggingface_pipeline_task, huggingface_model_reference',
    [
        ('feature-extraction','sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'),
    ]
)
@pytest.mark.parametrize(
    'neuron',
    [
        True,
        False # regular torchscript
    ]
)
@pytest.mark.parametrize(
    'batch_size',
    [
        1,
        4,
        8
    ]
)
@pytest.mark.parametrize(
    'max_length',
    [
        15,
        # None, # for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', this is 512 and takes a long time for neuron tracing
    ]
)
def test_compiled_feature_extraction_pipeline_from_pipeline(huggingface_pipeline_task, huggingface_model_reference, huggingface_pipeline, max_length, batch_size, neuron, sample_inputs, regression_test_atol, regression_test_rtol):
    
    # create compiled pipeline
    compiled_pipeline = CompiledPipeline.from_pipeline(
        huggingface_pipeline,
        max_length=max_length,
        batch_size=batch_size, 
        neuron=neuron,
        validate_compilation = True, 
        validation_rtol=regression_test_rtol, 
        validation_atol=regression_test_atol,
        tokenizer_settings={'add_special_tokens': True}
    )
    
    # score compiled pipeline
    compiled_pipeline_output: Tuple[Tuple[List[List[float]]]] = compiled_pipeline(sample_inputs) # 1 x n_batch x n_token x n_embed
    compiled_pipeline_output_arr: np.array = np.array(compiled_pipeline_output)
    
    # score huggingface pipeline
    huggingface_pipeline_output: Tuple[Tuple[List[List[float]]]] = huggingface_pipeline(
        sample_inputs, 
        tokenize_kwargs={
            'truncation':True,
            'add_special_tokens': True,
            'padding':'max_length',
            'max_length':max_length
            }
        ) # 1 x n_batch x n_token x n_embed
    huggingface_pipeline_output_arr: np.array = np.array(huggingface_pipeline_output)
    
    # validation: regression test embedding vectors
    np.testing.assert_allclose(compiled_pipeline_output_arr, huggingface_pipeline_output_arr, rtol=regression_test_rtol, atol=regression_test_atol)