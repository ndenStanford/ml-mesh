import pytest
from pytest_lazyfixture import lazy_fixture
from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
from libs.ml_compile.onclusiveml.tests.conftest import MODEL_MAX_LENGTH

@pytest.mark.parametrize(
    'tokenization_kwargs,expected_tokenization_settings',
    [
        (
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True}, 
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True, 'padding':'max_length', 'truncation': True, 'add_special_tokens': True, 'max_length': MODEL_MAX_LENGTH}
        ),
        (
            lazy_fixture('custom_tokenization_settings'), 
            lazy_fixture('custom_tokenization_settings')
        )
    ]
)
def test_compiled_tokenizer__init(mock_tokenizer, tokenization_kwargs, expected_tokenization_settings):
    
    print(expected_tokenization_settings)
    
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=mock_tokenizer,
        **tokenization_kwargs
    )
        
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings
    
@pytest.mark.parametrize(
    'tokenization_kwargs,expected_tokenization_settings',
    [
        (
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True}, 
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True, 'padding':'max_length', 'truncation': True, 'add_special_tokens': True, 'max_length': MODEL_MAX_LENGTH}),
        (
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True, 'padding':'some value', 'truncation': False, 'add_special_tokens': False, 'max_length': 20}, 
            {'setting_1': 'A', 'setting_2': 10, 'setting_3': True, 'padding':'some value', 'truncation': False, 'add_special_tokens': False, 'max_length': 20}
        )
    ]
)
def test_compiled_tokenizer__from_tokenizer(mock_tokenizer, tokenization_kwargs, expected_tokenization_settings):
    
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=mock_tokenizer,
        **tokenization_kwargs
    )
        
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings
    
    
def test_compiled_tokenizer_set_all_delegated_tokenizer_methods(compiled_tokenizer, all_delegated_method_references_with_sample_inputs):
    
    for delegated_method_reference, sample_input in all_delegated_method_references_with_sample_inputs:
        getattr(compiled_tokenizer,delegated_method_reference)(sample_input) == getattr(compiled_tokenizer.tokenizer,delegated_method_reference)(sample_input)