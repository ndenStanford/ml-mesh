from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast, AutoTokenizer
from transformers.utils.generic import PaddingStrategy
import os
import json
from typing import List, Union
from datetime import datetime as dt
import shutil
from functools import partial

class CompiledTokenizer(PreTrainedTokenizer, PreTrainedTokenizerFast):
    
    @classmethod
    def from_tokenizer(cls, tokenizer: PreTrainedTokenizer, **tokenization_kwargs) -> Union[PreTrainedTokenizer,PreTrainedTokenizerFast]:
        '''Takes a huggingface transformer tokenizer, compiles it according to specified
        configuration and returns a fully instantiated CompiledTokenizer instance.'''
        
        # export and re-import tokenizer to avoid changing in place
        local_temp_dir = f'temp_{dt.now().strftime(format="%Y_%m_%d__%H_%M_%s")}'
        tokenizer.save_pretrained(local_temp_dir)
        
        print(tokenizer.__class__)
        
        compiled_tokenizer = tokenizer.__class__.from_pretrained(local_temp_dir, read_specs=False)
        shutil.rmtree(local_temp_dir)
        
        # ensure the custom class's save_pretrained and configured_tokenize methods are used for the returned instance
        compiled_tokenizer.save_pretrained = partial(cls.save_pretrained, compiled_tokenizer) 
        compiled_tokenizer.configured_tokenize = partial(cls.configured_tokenize, compiled_tokenizer)
        
        # easy access attribute to verify whether a given tokenizer has been compiled
        compiled_tokenizer.compiled = True
        
        # ensure reasonable defaults and required specs for deterministic tokenization calls
        tokenization_settings = {}
        tokenization_settings['padding']: Union[bool, str, PaddingStrategy] = tokenization_kwargs.pop('padding','max_length')
        tokenization_settings['truncation']: bool = tokenization_kwargs.pop('truncation',True)
        tokenization_settings['add_special_tokens']: bool = tokenization_kwargs.pop('add_special_tokens',True)
        tokenization_settings['max_length']: int = tokenization_kwargs.pop('max_length',tokenizer.model_max_length)
        tokenization_settings.update(tokenization_kwargs)
        
        compiled_tokenizer.tokenization_settings = tokenization_settings
        
        return compiled_tokenizer
        
        
    def save_pretrained(self, directory):
        
        # if os.path.isfile(directory):
        #     print(f"Provided path ({directory}) should be a directory, not a file")
        #     return
        
        # os.makedirs(directory, exist_ok=True)

        self.__class__.save_pretrained(self, directory)
        
        with open(os.path.join(directory,'tokenization_settings.json'),'w') as tokenization_settings_file:
            json.dump(self.tokenization_settings,tokenization_settings_file)

    @classmethod
    def from_pretrained(cls, directory, read_specs: bool = True):
        
        compiled_tokenizer = AutoTokenizer.from_pretrained(directory)
        
        # ensure the custom class's save_pretrained and configured_tokenize methods are used for the returned instance
        compiled_tokenizer.save_pretrained = partial(cls.save_pretrained, compiled_tokenizer) 
        compiled_tokenizer.configured_tokenize = partial(cls.configured_tokenize, compiled_tokenizer)
        
        # easy access attribute to verify whether a given tokenizer has been compiled
        compiled_tokenizer.compiled = True
        
        if read_specs:
            with open(os.path.join(directory,'tokenization_settings.json'),'r') as compilation_specs_file:
                compiled_tokenizer.tokenization_settings = json.load(compilation_specs_file)
        
        return compiled_tokenizer
    
    def configured_tokenize(self, *args, **kwargs):
        '''Convenience to use the tokenization_settings attribute's content as overrides for the relevant kwargs. 
        This is to allow for easy deterministic and reproducible tokenization behaviour. Enabled by default,
        can be disabled by passing compilation_mode=False.'''

        for tokenization_setting in self.tokenization_settings:
            _ = kwargs.pop(tokenization_setting,None)
        kwargs.update(self.tokenization_settings)

        result = self.__call__(*args,**kwargs)
            
        return result