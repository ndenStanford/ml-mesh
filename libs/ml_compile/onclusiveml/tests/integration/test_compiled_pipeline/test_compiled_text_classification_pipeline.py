import pytest
from transformers import pipeline
from pytest_lazyfixture import lazy_fixture
from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
from libs.ml_compile.onclusiveml.ml_compile.compiled_model import CompiledModel
from typing import List, Tuple
import torch
import numpy as np
import pandas as pd


@pytest.mark.parametrize(
    'huggingface_pipeline_task, huggingface_model_reference',
    [
        ('text-classification','prajjwal1/bert-tiny')
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
@pytest.mark.parametrize(
    'tokenization_kwargs',
    [
        lazy_fixture('custom_tokenization_settings'),
    ]
)
def test_compiled_tokenizer_from_model(huggingface_pipeline_task, huggingface_model_reference, huggingface_pipeline, tokenization_kwargs, max_length, batch_size, neuron, sample_inputs, regression_test_atol, regression_test_rtol):
    
    # compile tokenizer
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=huggingface_pipeline.tokenizer,
        **tokenization_kwargs
    )
    
    # compile model including built-in validation on tracing inputs
    model_compilation_kwargs = {
        'batch_size':batch_size,
        'max_length':max_length,
        'neuron':neuron,  
    }
    
    compiled_model = CompiledModel.from_model(
        model=huggingface_pipeline.model,
        validate_compilation=True,
        validation_atol=regression_test_atol,
        validation_rtol=regression_test_rtol,
        **model_compilation_kwargs
    )
    
    # create new pipeline using compiled versions of tokenizer and model
    compiled_pipeline = pipeline(huggingface_pipeline_task, tokenizer=compiled_tokenizer, model=compiled_model)
    compiled_pipeline_output: Tuple[Tuple[List[List[float]]]] = compiled_pipeline(sample_inputs) # 1 x n_batch x n_token x n_embed
    
    # validate new pipeline via regression test
    huggingface_pipeline_output: Tuple[Tuple[List[List[float]]]] = huggingface_pipeline(sample_inputs, **tokenization_kwargs) # 1 x n_batch x n_token x n_embed
    
    huggingface_pipeline_output_df = pd.DataFrame(huggingface_pipeline_output)
    compiled_pipeline_output_df = pd.DataFrame(compiled_pipeline_output)
    
    pd.testing.assert_series_equal(huggingface_pipeline_output_df['label'], compiled_pipeline_output_df['label'])
    np.testing.assert_allclose(huggingface_pipeline_output_df['score'].values, compiled_pipeline_output_df['score'].values, rtol=regression_test_rtol, atol=regression_test_atol)