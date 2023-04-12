import pytest
from libs.ml_compile.onclusiveml.ml_compile.compiled_model import CompiledModel
import torch
import torch.neuron
import shutil

@pytest.mark.parametrize(
    'huggingface_model_reference',
    [
        #'prajjwal1/bert-tiny',
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    ]
)
@pytest.mark.parametrize(
    'neuron',
    [
        True,
        #False # regular torchscript
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
        10,
        # None, # for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', this is 512 and takes a long time for neuron tracing
    ]
)
def test_compiled_tokenizer_from_pretrained(huggingface_tokenizer, huggingface_model, batch_size, max_length, neuron, sample_inputs, regression_test_atol, regression_test_rtol):
        
    # compile model including built-in validation on tracing inputs
    kwargs = {
        'batch_size':batch_size,
        'max_length':max_length,
        'neuron':neuron,
    }
    
    compiled_model = CompiledModel.from_model(
        model=huggingface_model,
        validate_compilation=True,
        validation_atol=regression_test_atol,
        validation_rtol=regression_test_rtol,
        **kwargs
    )
    
    compiled_model.save_pretrained('test_compiled_model')
    reloaded_compiled_model = CompiledModel.from_pretrained('test_compiled_model')
    
    # additional, regression based validation with custom tokenizer & inputs
    sample_tokens = huggingface_tokenizer(sample_inputs, return_tensors='pt', max_length=max_length, padding='max_length',truncation=True)
    compiled_model_output = compiled_model(**sample_tokens)[0] # ignore gradient at position 1
    reloaded_compiled_model_output = reloaded_compiled_model(**sample_tokens)[0] # ignore gradient at position 1
    
    torch.testing.assert_close(compiled_model_output, reloaded_compiled_model_output, atol=regression_test_atol, rtol=regression_test_rtol)
    
    shutil.rmtree('test_compiled_model')