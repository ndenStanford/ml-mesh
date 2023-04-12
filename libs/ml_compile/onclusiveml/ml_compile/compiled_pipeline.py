from transformers.pipelines import Pipeline, pipeline
from typing import Dict
from libs.ml_compile.onclusiveml.ml_compile.compile_utils import duplicate_huggingface_transformer_via_local_cache
from libs.ml_compile.onclusiveml.ml_compile.compiled_tokenizer import CompiledTokenizer
from libs.ml_compile.onclusiveml.ml_compile.compiled_model import CompiledModel
import os
import json

class CompiledPipeline(object):
    '''A wrapper class around huggingface pipeline instances with custom CompiledTokenizer and CompiledModel backends. 
    Includes
    - canonical `save_pretrained` & `load_pretrained` methods to support export & re-import to/from local disk
    - utility `from_pipeline` method to wrap around the creation of CompiledTokenizer and CompiledModel
        instances, respectively, using provided generic huggingface tokenizer and model instances
    - canonical __call__ method delegating to Pipeline type compiled_pipeline attribute for inference.'''
    
    def __init__(
        self,
        original_pipeline: Pipeline,
        compiled_pipeline: Pipeline
    ):
        
        self.original_pipeline = original_pipeline
        self.original_pipeline_task = original_pipeline.task
        self.compiled_pipeline = compiled_pipeline
        
    @classmethod
    def from_pipeline(
        cls, 
        pipeline: Pipeline,
        max_length: int,
        batch_size: int = 1, 
        neuron: bool=True,
        validate_compilation: bool = True, 
        validation_rtol: float = 1e-02, 
        validation_atol: float = 1e-02,
        tokenizer_settings: Dict = {},
        model_tracing_settings: Dict = {}
    ):
        
        original_pipeline = duplicate_huggingface_transformer_via_local_cache(pipeline)
        compiled_pipeline = compile_pipeline(
            pipeline=pipeline,
            max_length=max_length,
            batch_size=batch_size, 
            neuron=neuron,
            validate_compilation=validate_compilation, 
            validation_rtol=validation_rtol, 
            validation_atol=validation_atol,
            tokenizer_setting=tokenizer_settings,
            model_tracing_settings=model_tracing_settings,
            in_place_compilation=True
        )
        
        return cls(
            original_pipeline=original_pipeline,
            compiled_pipeline=compiled_pipeline
        )
        
    def save_pretrained(self, directory):

        # export original uncompiled pipeline
        self.original_pipeline.save_pretrained(os.path.join(directory,'pipeline'))
        
        # export pipeline task
        with open(os.path.join(directory,'pipeline_task.json'),'w') as pipeline_task_file:
            json.dump({'task':self.original_pipeline_task},pipeline_task_file)
        
        # export compiled tokenizer
        self.compiled_pipeline.tokenizer.save_pretrained(os.path.join(directory,'compiled_tokenizer'))
        
        # export compiled model
        self.compiled_pipeline.model.save_pretrained(os.path.join(directory,'compiled_model'))
            
    @classmethod
    def from_pretrained(cls, directory):
    
       # import pipeline task
        with open(os.path.join(directory,'pipeline_task.json'),'r') as pipeline_task_file:
            pipeline_task = json.load(pipeline_task_file)['task']

        # use imported pipeline task to import original uncompiled pipeline
        original_pipeline = pipeline(task=pipeline_task, model=os.path.join(directory,'pipeline'))
        
        compiled_pipeline = duplicate_huggingface_transformer_via_local_cache(original_pipeline)
        
        # import and insert compiled tokenizer into designated attribute
        compiled_pipeline.tokenizer = CompiledTokenizer.from_pretrained(os.path.join(directory,'compiled_tokenizer'))
        
        # export and insert compiled model into designated attribute
        compiled_pipeline.model = CompiledModel.from_pretrained(os.path.join(directory,'compiled_model'))
                
        return cls(
            original_pipeline=original_pipeline,
            compiled_pipeline=compiled_pipeline
        )
    
    def __call__(self, *args, **kwargs):
        '''Provide entrypoiny to the compiled_pipeline attribute's __call__ method.'''
        
        return self.compiled_pipeline(*args,**kwargs)
    

def compile_pipeline(
    pipeline: Pipeline,
    max_length: int,
    batch_size: int = 1, 
    neuron: bool=True,
    validate_compilation: bool = True, 
    validation_rtol: float = 1e-02, 
    validation_atol: float = 1e-02,
    tokenizer_settings: Dict = {},
    model_tracing_settings: Dict = {},
    in_place_compilation: bool = False,
    **kwargs
) -> Pipeline:
    """Utility function to take a conventional huggingface transformers pipeline and replace
    - its tokenizer with a CompiledTokenizer instance of the same object
    - its model component with a CompiledModel instance of the same oject
    to produce a manipulated pipeline instance of the same class as the specified pipeline
    obejct, without changing it in place. The manipulated pipeline instance will have
    fully functional import and export functionality, as well as a __call__ behaviour
    that 'just works' with its (neuron-)torchscript model backend. Currently supported
    pipeline tasks include:
    - feature-extraction
    - text-classification (aka sentiment-analysis)"""

    # get copy of passed pipeline instance if needed
    if not in_place_compilation:
        compiled_pipeline = duplicate_huggingface_transformer_via_local_cache(pipeline)
    else:
        compiled_pipeline = pipeline
    
    # overwrite potential max_length value in the tokenizer settings to ensure alignment with compiled model
    tokenizer_settings['max_length'] = max_length
    
    # attach compiled tokenizer
    compiled_pipeline.tokenizer = CompiledTokenizer.from_tokenizer(tokenizer=pipeline.tokenizer, **tokenizer_settings)
    
    # compile model and attached compiled model
    compiled_pipeline.model = CompiledModel.from_model(
        pipeline.model, 
        batch_size=batch_size,
        max_length=max_length,
        neuron=neuron,
        validate_compilation=validate_compilation, 
        validation_rtol=validation_rtol, 
        validation_atol=validation_atol,
        **model_tracing_settings
    )
    
    return compiled_pipeline