import pytest
from pytest_lazyfixture import lazy_fixture
from transformers import AutoTokenizer
from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
import shutil

@pytest.mark.parametrize(
    'huggingface_model_reference',
    [
        'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
    ]
)
@pytest.mark.parametrize(
    'tokenization_kwargs,expected_tokenization_settings',
    [
        (
            {}, 
            {'padding':'max_length', 'truncation': True, 'add_special_tokens': True} # max_length is set inside the test
        ),
        (
            lazy_fixture('custom_tokenization_settings_1'), 
            lazy_fixture('custom_tokenization_settings_1')
        ),
        (
            lazy_fixture('custom_tokenization_settings_2'), 
            lazy_fixture('custom_tokenization_settings_2')
        ),
        (
            lazy_fixture('custom_tokenization_settings_3'), 
            lazy_fixture('custom_tokenization_settings_3')
        )
    ]
)
def test_compiled_tokenizer__init(huggingface_tokenizer, tokenization_kwargs, expected_tokenization_settings, huggingface_model_max_length, all_delegated_method_references_with_sample_inputs):
        
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=huggingface_tokenizer,
        **tokenization_kwargs
    )
    
    compiled_tokenizer.save_pretrained('test_compiled_tokenizer')
    reloaded_compiled_tokenizer = compiled_tokenizer.from_pretrained('test_compiled_tokenizer')
    
    # --- validation suite: reloaded compiled tokenizer against original compiled tokenizer
    # for ground truth, set the only tokenization settings value that depends on the huggingface reference model
    if 'max_length' not in tokenization_kwargs:
        expected_tokenization_settings['max_length'] = huggingface_model_max_length
    
    # validate tokenization settings
    assert reloaded_compiled_tokenizer.tokenization_settings == compiled_tokenizer.tokenization_settings
    
    # validate delegated tokenization methods of reloaded compiled tokenizer against equivalent methods of original compiled tokenizer
    for delegated_method_reference, sample_input in all_delegated_method_references_with_sample_inputs:
        assert getattr(reloaded_compiled_tokenizer,delegated_method_reference)(sample_input) == getattr(compiled_tokenizer,delegated_method_reference)(sample_input)
        
    # validate configured __call__ method of reloaded compiled tokenizer against original compiled tokenizer's __call__ method
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][1] # text string for tokenizer() call
    assert compiled_tokenizer(tokenization___call___input) == compiled_tokenizer.tokenizer(tokenization___call___input,**compiled_tokenizer.tokenization_settings)
    
    # clean up local dir
    shutil.rmtree('test_compiled_tokenizer')