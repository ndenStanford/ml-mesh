import pytest
from pytest_lazyfixture import lazy_fixture
from transformers import AutoTokenizer
from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
from libs.ml_compile.onclusiveml.tests.functional.conftest import MODEL_MAX_LENGTH


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
    
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=huggingface_tokenizer,
        **tokenization_kwargs
    )
    
    # --- validation suite: compiled tokenizer against passed mock tokenizer and expected ground truths
    # for ground truth, set the only tokenization settings value that depends on the huggingface reference model
    if 'max_length' not in tokenization_kwargs:
        expected_tokenization_settings['max_length'] = huggingface_model_max_length
    
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings
    
    # validate delegated tokenization methods
    for delegated_method_reference, sample_input in all_delegated_method_references_with_sample_inputs:
        assert getattr(compiled_tokenizer,delegated_method_reference)(sample_input) == getattr(huggingface_tokenizer,delegated_method_reference)(sample_input)
        
    # validate configured __call__ method
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][1] # text string for tokenizer() call
    assert compiled_tokenizer(tokenization___call___input) == compiled_tokenizer.tokenizer(tokenization___call___input,**compiled_tokenizer.tokenization_settings)