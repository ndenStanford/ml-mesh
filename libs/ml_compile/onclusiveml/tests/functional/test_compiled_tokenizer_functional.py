from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
from transformers import AutoTokenizer

def test_compiled_tokenizer_pretrained(compiled_tokenizer, mock_tokenizer, monkeypatch):
    
    compiled_tokenizer.save_pretrained('test_compiled_tokenizer')
    
    # monkey patch transformers.AutoTokenizer.from_pretrained so our mock_tokenizer can be loaded
    def mock_from_pretrained(directory: str):
        return mock_tokenizer.from_pretrained(directory)
    
    monkeypatch.setattr(AutoTokenizer, "from_pretrained", mock_from_pretrained)
    
    reloaded_test_compiled_tokenizer = CompiledTokenizer.from_pretrained('test_compiled_tokenizer')
    
    compiled_tokenizer.tokenizer == reloaded_test_compiled_tokenizer.tokenizer
    compiled_tokenizer.tokenization_settings == reloaded_test_compiled_tokenizer.tokenization_settings