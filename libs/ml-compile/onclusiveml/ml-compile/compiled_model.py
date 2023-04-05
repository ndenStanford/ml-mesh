import os
import torch
from transformers import AutoConfig
from transformers.modeling_outputs import BaseModelOutput
from transformers.modeling_utils import PreTrainedModel
from transformers.utils.generic import ModelOutput
from typing import List


class CompiledModel(PreTrainedModel):

    @classmethod
    def from_model(cls, model, batch_size: int = 1, max_length: int = None, neuron: bool=True, **tracing_kwargs):
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
            
        tracing_kwargs['dynamic_batch_size']: bool = tracing_kwargs.get('dynamic_batch_size',True)
        tracing_kwargs['strict']: bool = tracing_kwargs.get('strict',True)
        tracing_kwargs['compiler_args']: List[str] = tracing_kwargs.get('compiler_args',['--fast-math','none'])
        
        # trace model and return fuilly functional custom model class instance
        compiled_model = compile_model(model, batch_size=batch_size, max_length=max_length, neuron=neuron, **tracing_kwargs)

        return compiled_model

    # def prepare_inputs_for_generation(
    #         self,
    #         input_ids,
    #         encoder_outputs=None,
    #         attention_mask=None,
    #         **kwargs,
    # ):
    #     # Pad the inputs for Neuron
    #     current_length = input_ids.shape[1]
    #     pad_size = self.config.max_length - current_length
    #     return dict(
    #         input_ids=F.pad(input_ids, (0, pad_size)),
    #         attention_mask=attention_mask,
    #         encoder_outputs=encoder_outputs.last_hidden_state,
    #         current_length=torch.tensor(current_length - 1),
    #     )

    # def get_encoder(self):
    #     def encode(input_ids, attention_mask, **kwargs):
    #         output, = self.encoder(input_ids, attention_mask)
    #         return BaseModelOutput(
    #             last_hidden_state=output,
    #         )
    #     return encode

    def forward(self, input_ids, attention_mask, **kwargs):

        model_output = self.model(input_ids, attention_mask)
        
        if isinstance(model_output, dict):
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

    @classmethod
    def from_pretrained(cls, directory):
        config = AutoConfig.from_pretrained(directory)
        
        compiled_model = cls(config)
        compiled_model.model = torch.jit.load(os.path.join(directory, 'model.pt'))
        
        return compiled_model
    
def compile_model(model, batch_size: int, max_length: int,  neuron: bool = True, **tracing_kwargs):
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
        torch.ones((batch_size, max_length), dtype=torch.long), # input_ids
        torch.ones((batch_size, max_length), dtype=torch.long) # attention_mask
    )
    
    print('tracing_kwargs:', tracing_kwargs)
    
    if neuron:
        traced_model = torch.neuron.trace(model,tracing_inputs, **tracing_kwargs)
    else:
        traced_model = torch.jit.trace(model, tracing_inputs, **tracing_kwargs)
        
    compiled_model = CompiledModel(model.config)
    compiled_model.model = traced_model
    
    return compiled_model