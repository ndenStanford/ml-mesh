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
        instances, respectively, using provided generic huggingface tokenizer and model instances, by
        applying a pipeline level utility compilaiton function to a specified huggingface pipeline instance
    - canonical __call__ method delegating to Pipeline type compiled_pipeline attribute for inference.'''
    
    def __init__(
        self,
        original_pipeline: Pipeline,
        compiled_pipeline: Pipeline
    ):
        '''Constructor requires 
        - `original_pipeline`, the original reference huggingface pipeline
        - `compiled_pipeline`, the manipulated pipeline with compiled tokenizer and model backends'''
        
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
        '''Takes a huggingface transformer pipeline, compiles 
        - the `tokenizer` attribute to a CompiledTokenizer instance
        - the `model` attribute to a CompiledModel instance
        according to specified configuration and returns a fully instantiated CompiledPipeline instance together with
        the (neuron-)tracing configurations used during the compilation for both components.
        
        pipeline (Pipeline): Pipeline instance that needs to be compiled. Can be manipulated in place if desired, 
        but by default a copy will be made.
        max_length (int): The max token sequence length used for compilation of both tokenizer and model.
        batch_size (int): The batch size used for model compilation. Defaults to 1. 
        neuron (int): If True, uses the AWS neuron library to convert the pipeline's model component to neuron-torchscript
            for faster inference. If False, uses native torch to produce a torchscript model. Defaults to True.
        validate_compilation (bool): If True, a quick regression test of the compiled model is made using the inputs
            used for compilation. Acceptance thresholds of that regression test are set by the optional arguments
                - `validation_rtol`, and
                - `validation_atol`.
            Defaults to True
        validation_rtol (float): See `validate_compilation`. Defaults to 1e-02. 
        validation_atol (float): See `validate_compilation`. Defaults to 1e-02.
        tokenizer_settings (dict): (optional) the dictionary equivalent of the CompiledTokenzer.from_tokenizer's 
            **tokenization_kwargs.
        model_tracing_settings (dict): The dictionary equivalent of the CompiledModel.from_model`s 
            **tracing_kwargs.'''
        
        # avoid manipulating passed pipeline instance in place
        original_pipeline = duplicate_huggingface_transformer_via_local_cache(pipeline)
        
        # replace the tokenizer and model components with compiled equivalents
        compiled_pipeline = compile_pipeline(
            pipeline=original_pipeline,
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
        '''Canonic huggingface transformers export method. Only supports exporting to local file system.'''
        
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
        '''Canonic huggingface transformers export method. Only supports importing from local file system.'''
    
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
        '''Provides entrypoint to the `compiled_pipeline` attribute's __call__ method.
        Useage is identical to canonical huggingface pipeline __call__ method.'''
        
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
    - its tokenizer with a CompiledTokenizer instance version of the same object
    - its model component with a CompiledModel instance version of the same oject
    to produce a manipulated pipeline instance of the same class as the specified pipeline
    object, without changing it in place (unless desired). The manipulated pipeline instance will have
    fully functional import and export functionality, as well as a __call__ behaviour
    that 'just works' with its (neuron-)torchscript model backend. Currently supported
    pipeline tasks include:
    - feature-extraction
    - text-classification (aka sentiment-analysis)
    
    pipeline (Pipeline): Pipeline instance that needs to be compiled. Can be manipulated in place if desired, 
        but by default a copy will be made.
    max_length (int): The max token sequence length used for compilation of both tokenizer and model.
    batch_size (int): The batch size used for model compilation. Defaults to 1. 
    neuron (int): If True, uses the AWS neuron library to convert the pipeline's model component to neuron-torchscript
        for faster inference. If False, uses native torch to produce a torchscript model. Defaults to True.
    validate_compilation (bool): If True, a quick regression test of the compiled model is made using the inputs
        used for compilation. Acceptance thresholds of that regression test are set by the optional arguments
            - `validation_rtol`, and
            - `validation_atol`.
        Defaults to True
    validation_rtol (float): See `validate_compilation`. Defaults to 1e-02. 
    validation_atol (float): See `validate_compilation`. Defaults to 1e-02.
    tokenizer_settings (dict): (optional) the dictionary equivalent of the CompiledTokenzer.from_tokenizer's 
        **tokenization_kwargs.
    model_tracing_settings (dict): The dictionary equivalent of the CompiledModel.from_model`s 
        **tracing_kwargs.
    in_place_compilation (bool): If True, will edit the passed `pipeline` object in place. If False, will use local
        cache to create a duplicate. Defaults to False.
    """

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