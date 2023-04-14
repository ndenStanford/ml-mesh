import pytest
from pytest_lazyfixture import lazy_fixture
from transformers import AutoTokenizer
from onclusiveml.ml_compile import CompiledTokenizer
import shutil

@pytest.mark.parametrize(
    'tokenization_kwargs',
    [
        {'setting_1': 'A', 'setting_2': 10, 'setting_3': True},
        lazy_fixture('custom_tokenization_settings'),
    ]
)
def test_compiled_tokenizer__from_pretrained(mock_tokenizer, tokenization_kwargs, monkeypatch, all_delegated_method_references_with_sample_inputs):
    
    # --- export compiled tokenizer to local
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=mock_tokenizer,
        **tokenization_kwargs
    )
    
    compiled_tokenizer.save_pretrained('test_compiled_tokenizer')
    
    # --- re-import compiled tokenizer from local
    # monkey patch transformers.AutoTokenizer.from_pretrained so our mock_tokenizer can be loaded
    def mock_from_pretrained(directory: str):
        return mock_tokenizer.from_pretrained(directory)
    
    monkeypatch.setattr(AutoTokenizer, "from_pretrained", mock_from_pretrained)
    
    reloaded_test_compiled_tokenizer = CompiledTokenizer.from_pretrained('test_compiled_tokenizer')
    
    # --- validation suite: reloaded compiled tokenizer against original compiled tokenizer
    # validate tokenization settings
    assert reloaded_test_compiled_tokenizer.tokenization_settings == compiled_tokenizer.tokenization_settings
    
    # validate delegated tokenization methods of reloaded compiled tokenizer against equivalent methods of original compiled tokenizer
    for delegated_method_reference, sample_input in all_delegated_method_references_with_sample_inputs:
        assert getattr(reloaded_test_compiled_tokenizer,delegated_method_reference)(sample_input) == getattr(compiled_tokenizer.tokenizer,delegated_method_reference)(sample_input)
        
    # validate configured __call__ method of reloaded compiled tokenizer against original compiled tokenizer's __call__ method
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][1] # text string for tokenizer() call
    assert reloaded_test_compiled_tokenizer(tokenization___call___input) == compiled_tokenizer(tokenization___call___input)
    
    # clean up local dir
    shutil.rmtree('test_compiled_tokenizer')