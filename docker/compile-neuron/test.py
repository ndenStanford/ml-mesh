import pytest
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import sys

def test_imports():
    
    import torch_neuron
    
def test_neuron_compile_torch_function():

    def foo(x, y):
        return 2 * x + y

    inputs = (torch.rand(3), torch.rand(3))

    # Run `foo` with the provided inputs and record the tensor operations
    traced_foo = torch.neuron.trace(foo, inputs)

    # `traced_foo` can now be run with the TorchScript interpreter or saved
    # and loaded in a Python-free environment
    torch.jit.save(traced_foo, os.path.join('/output','traced_foo.pt'))
    
def test_neuron_compile_torch_graph():
    
    class Net(torch.nn.Module):
        
        def __init__(self):
            super(Net, self).__init__()
            self.conv = torch.nn.Conv2d(1, 1, 3)

        def forward(self, x):
            return self.conv(x) + 1

    n = Net()
    n.eval()

    inputs = torch.rand(1, 1, 3, 3)

    # Trace a specific method and construct `ScriptModule` with
    # a single `forward` method
    neuron_forward = torch.neuron.trace(n.forward, inputs)
    torch.jit.save(neuron_forward, os.path.join('/output','neuron_forward.pt'))

    # Trace a module (implicitly traces `forward`) and constructs a
    # `ScriptModule` with a single `forward` method
    neuron_net = torch.neuron.trace(n, inputs)
    torch.jit.save(neuron_net, os.path.join('/output','neuron_net.pt'))
    
@pytest.mark.parametrize(
    'model_name, dynamic_batch_size',
    [
        ('resnet50',False),
        ('resnet50',True)
    ]
)
def test_neuron_compile_torch_vision_model(model_name, image_tracing_input, dynamic_batch_size):

    # Load the model and set it to evaluation mode
    model = torch.hub.load("pytorch/vision", model_name, pretrained=True)
    #model = cv_models.resnet50(pretrained=True)
    model.eval()

    # Compile with an example input of batch size 1    
    model_neuron = torch.neuron.trace(
        model,
        image_tracing_input,
        dynamic_batch_size=dynamic_batch_size
    )
    
    torch.jit.save(
        model_neuron, 
        os.path.join('/output',f'torch_vision_model_neuron_{dynamic_batch_size}.pt')
    )


@pytest.mark.parametrize(
    'model_name, language_modelling_head, dynamic_batch_size',
    [
        ('bert-base-uncased','modelForSequenceClassification',False),
        ('bert-base-uncased','modelForSequenceClassification',True),
        ('bert-base-uncased','model',False),
        ('bert-base-uncased','model',True)
    ]
)
def test_neuron_compile_torch_nlp_model(model_name, language_modelling_head, text_tracing_input, dynamic_batch_size):

    tokenizer = torch.hub.load('huggingface/pytorch-transformers', 'tokenizer', model_name)
    model = torch.hub.load('huggingface/pytorch-transformers', language_modelling_head, model_name)
    model.eval()
    
    token_tracing_input = tokenizer.encode(text_tracing_input, add_special_tokens=True)
        
    # neuron trace model
    neuron_model = torch.neuron.trace(
        model, 
        *token_tracing_input,
        compiler_args='-O2', 
        optimize = 'aggressive'
    )
    
    # export neuron traced model
    torch.jit.save(
        neuron_model,
        os.path.join('/output',f'torch_nlp_model_neuron_{model_name}_{language_modelling_head}_{dynamic_batch_size}.pt')    
    )
    

@pytest.mark.parametrize(
    'model_name, dynamic_batch_size',
    [
        ('distilbert-base-uncased',False),
        ('distilbert-base-uncased',True)
    ]
)
def test_neuron_compile_transformer_nlp_model(model_name, text_tracing_input, dynamic_batch_size):
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.eval()
    
    token_tracing_input = tokenizer.encode(text_tracing_input, add_special_tokens=True)
    
    model_neuron = torch.neuron.trace(
        model,
        *token_tracing_input,
        compiler_args='-O2', 
        optimize = 'aggressive'
    )
    
    torch.jit.save(
        model_neuron,
        os.path.join('/output',f'transformer_nlp_model_neuron_{model_name}_{dynamic_batch_size}.pt')
    )