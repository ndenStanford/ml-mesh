from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast, AutoTokenizer
from libs.ml_compile.onclusiveml.ml_compile.compile_utils import duplicate_huggingface_transformer_via_local_cache
import os
import json
from typing import Union, Any, Dict
    
class CompiledTokenizer(object):
    '''A wrapper class around huggingface Tokenizer instances that supports reproducible tokenization. Includes extension of 
    save_pretrained & load_pretrained methods to specified tokenization parameters and a __call__ method that will override
    kwargs in favour of those tokenization parameters. Useful in combination with (neuron-)compiled models, and the
    CompiledModel class with or without the use of transformer Pipelines.'''
    
    def __init__(self, tokenizer: Union[PreTrainedTokenizer,PreTrainedTokenizerFast], **tokenization_kwargs):
        
        self.tokenizer = duplicate_huggingface_transformer_via_local_cache(tokenizer)
        self.tokenization_settings = self.get_tokenization_settings(tokenizer, **tokenization_kwargs)
        self.compiled = True
        
        # attach base suite of delegated methods implemented by the hf tokenizer to preserve most of 
        # the common methods and simulate subclassig w.r.t available methods
        self.set_all_delegated_tokenizer_methods(tokenizer)
    
    @classmethod
    def get_tokenization_settings(cls, tokenizer: Union[PreTrainedTokenizer,PreTrainedTokenizerFast], **tokenization_kwargs) -> Dict[str,Any]:
        '''Sets some reasonable defaults for the params that define tokenization behaviour, in particular the 
        padding and sequence length of the resulting tokenized sequences.'''
        
        # ensure reasonable defaults and required specs for deterministic tokenization calls
        tokenization_settings = {}
        
        # ensure constant sequence length of outputs as per 
        # https://awsdocs-neuron.readthedocs-hosted.com/en/latest/src/examples/tensorflow/huggingface_bert/huggingface_bert.html#Compile-the-model-into-an-AWS-Neuron-Optimized-Model
        tokenization_settings['padding'] = 'max_length'
        tokenization_settings['truncation'] = True
        
        # ensure reasonable defaults
        tokenization_settings['add_special_tokens']: bool = tokenization_kwargs.pop('add_special_tokens',True)
        tokenization_settings['max_length']: int = tokenization_kwargs.pop('max_length',tokenizer.model_max_length)
        
        tokenization_settings.update(tokenization_kwargs)
        
        return tokenization_settings
    
    def set_all_delegated_tokenizer_methods(self, tokenizer: Union[PreTrainedTokenizer,PreTrainedTokenizerFast]):
        
        for tokenizer_method_reference in (
            'encode_plus',
            'encode',
            'decode',
            'create_token_type_ids_from_sequences',
            'convert_tokens_to_string',
            'clean_up_tokenization'
        ):
            self.set_delegated_tokenizer_method(tokenizer, tokenizer_method_reference)
    
    def set_delegated_tokenizer_method(self, tokenizer: Union[PreTrainedTokenizer,PreTrainedTokenizerFast], tokenizer_method_reference: str):
        
        # retrieve the target method from the attached huggingface tokenizer instance
        tokenizer_method = getattr(tokenizer, tokenizer_method_reference)
        
        # attach method to CompiledTokenizer instance
        setattr(self, tokenizer_method_reference, tokenizer_method)
    
    @classmethod
    def from_tokenizer(cls, tokenizer: Union[PreTrainedTokenizer,PreTrainedTokenizerFast], **tokenization_kwargs):
        '''Utility method wrapper around the constructor for consistency with the CompiledModel equivalent method.'''
        
        return CompiledTokenizer(
            tokenizer=tokenizer,
            **tokenization_kwargs
        )
    
    def save_pretrained(self, directory):

        # invoke parent class' instance method
        self.tokenizer.save_pretrained(directory)
        
        with open(os.path.join(directory,'tokenization_settings.json'),'w') as tokenization_settings_file:
            json.dump(self.tokenization_settings,tokenization_settings_file)
            
    @classmethod
    def from_pretrained(cls, directory, read_tokenization_settings=True):
    
        # invoke parent class' class method
        tokenizer = AutoTokenizer.from_pretrained(directory)
        
        if read_tokenization_settings:
            with open(os.path.join(directory,'tokenization_settings.json'),'r') as compilation_specs_file:
                tokenization_settings = json.load(compilation_specs_file)
                
        return CompiledTokenizer(
            tokenizer=tokenizer,
            **tokenization_settings
        )
    
    def __call__(self, *args, **kwargs):
        '''Overwrite the tokenizer's call dunder kwargs with the settings contained in the tokenization_settings attribute. 
        Makes configured tokenization as per compilation arguments the default, i.e. no need to remember the exact padding 
        and length configurations at the tokenization state.'''
        
        for tokenization_setting in self.tokenization_settings:
            _ = kwargs.pop(tokenization_setting,None)
        
        kwargs.update(self.tokenization_settings)
        
        return self.tokenizer(*args,**kwargs)