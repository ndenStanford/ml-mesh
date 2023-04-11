import os
import torch
from transformers import AutoConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.utils.generic import ModelOutput
from typing import List, Type, Type, Tuple, Dict, Any
import json


class CompiledModel(PreTrainedModel):
    '''A fully functional subclass from the huggingface PreTrainedModel using a (neuron-)torchscript model as backend. 
    Includes ( neuron-)torchscript utilities for automatic tracing of a specified pytorch model or huggingface transformer
    model. Also supports the persistence of key (neuron-)tracing configuration parameters.'''

    @classmethod
    def from_model(
        cls, 
        model: PreTrainedModel, 
        batch_size: int = 1, 
        max_length: int = None, 
        neuron: bool=True,
        validate_compilation: bool = True, 
        validation_rtol: float = 1e-02, 
        validation_atol: float = 1e-02,
        **tracing_kwargs) -> Type[PreTrainedModel]:
        '''Takes a huggingface transformer model, compiles it according to specified
        configuration and returns a fully instantiated CompiledModel instance.
        
        model (_type_): The huggingface pytorch model or pytorch nn.module to compile
        batch_size (_type_): The size of the batch used for tracing
        max_length (_type_): The number of tokens per record used for tracing, e.g. input sequence length
        neuron (bool, optional): _description_. If True, uses torch.neuron.trace for compilation,
            otherwise uses torch.jit.trace. Defaults to True.
        **tracing_kwargs:
            dynamic_batching (bool, optional): If True, traced model allows for 
                variable batch sizes during inference up to the batch_size used during compilation.
                Defaults to True.
            strict (bool, optional): If True, enforces deterministic inference behaviour during tracing. In 
                particular, requires the model arg to have return_dict=False.
            compiler_args (List[str], optional): Note: Not setting these was 
                observed to lead to NaN during inference on huggingface==4.27.x & torch==1.12.1. 
                Defaults to ['--fast-math','none'].
        '''
        
        # ensure reasonable defaults and required specs for functional neuron tracing
        if max_length is None:
            max_length = model.config.max_position_embeddings
        
        if neuron is True:
            tracing_kwargs['dynamic_batch_size']: bool = tracing_kwargs.get('dynamic_batch_size',True)
            tracing_kwargs['compiler_args']: List[str] = tracing_kwargs.get('compiler_args',['--fast-math','none'])
    
        tracing_kwargs['strict']: bool = tracing_kwargs.get('strict',False)
                
        # trace model and return fuilly functional custom model class instance
        traced_model, tracing_inputs, compilation_specs = compile_model(model, batch_size=batch_size, max_length=max_length, neuron=neuron, **tracing_kwargs)
        
        compiled_model = cls(model.config)
        compiled_model.model = traced_model
        compiled_model.compilation_specs = compilation_specs
        
        if validate_compilation is True:
            tracing_inputs_dict = {'input_ids': tracing_inputs[0], 'attention_mask': tracing_inputs[1]}
            model_output = model(**tracing_inputs_dict)[0]
            traced_model_output = compiled_model(**tracing_inputs_dict)[0]
        
            assert torch.allclose(model_output,traced_model_output, atol=validation_atol, rtol=validation_rtol)

        return compiled_model

    def forward(self, input_ids, attention_mask, **kwargs):

        model_output = self.model(input_ids, attention_mask)
        
        if isinstance(model_output, dict):
            print('Model output is a dictionary. Converting')
            model_output = ModelOutput(model_output)
            
        return model_output

    @property
    def device(self):  # Attribute required by beam search
        return torch.device('cpu')

    def save_pretrained(self, directory):
        if os.path.isfile(directory):
            print(f"Provided path ({directory}) should be a directory, not a file")
            return
        os.makedirs(directory, exist_ok=True)
        torch.jit.save(self.model, os.path.join(directory, 'model.pt'))
        self.config.save_pretrained(directory)
        
        with open(os.path.join(directory,'compilation_specs.json'),'w') as compilation_specs_file:
            json.dump(self.compilation_specs,compilation_specs_file)

    @classmethod
    def from_pretrained(cls, directory):
        config = AutoConfig.from_pretrained(directory)
        
        compiled_model = cls(config)
        compiled_model.model = torch.jit.load(os.path.join(directory, 'model.pt'))
        
        with open(os.path.join(directory,'compilation_specs.json'),'r') as compilation_specs_file:
            compiled_model.compilation_specs = json.load(compilation_specs_file)
        
        return compiled_model
    
def compile_model(
    model, 
    batch_size: int, 
    max_length: int,  
    neuron: bool = True, 
    **tracing_kwargs
    ) -> Tuple[torch.jit._trace.TopLevelTracedModule, Tuple[torch.Tensor, torch.Tensor], Dict[str,Any]]:
    """Traces a torch hf model to either torchscript or neuron torchscript, 
    then wraps it in the convenience CompiledModel class.

    Args:
        model (_type_): The huggingface pytorch model or pytorch nn.module to compile
        batch_size (_type_): The size of the batch used for tracing
        max_length (_type_): The number of tokens per record used for tracing, e.g. input sequence length
        neuron (bool, optional): _description_. If True, uses torch.neuron.trace for compilation,
            otherwise uses torch.jit.trace. Defaults to True.
    """
    
    # generate tracing inputs according to specs
    tracing_inputs = (
        torch.zeros((batch_size, max_length), dtype=torch.long), # input_ids
        torch.zeros((batch_size, max_length), dtype=torch.long) # attention_mask
    )
    
    if neuron:
        traced_model = torch.neuron.trace(model,tracing_inputs, **tracing_kwargs)
    else:
        traced_model = torch.jit.trace(model, tracing_inputs, **tracing_kwargs)
        
    compilation_specs = {'tracing_kwargs':tracing_kwargs.copy()}
    compilation_specs.update(
        {
            'tracing__batch_size':batch_size,
            'tracing__max_length':max_length,
            'tracing__neuron':neuron,
        }
    )
    
    return traced_model, tracing_inputs, compilation_specs