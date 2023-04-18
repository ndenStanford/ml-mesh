# Standard Library
import os
from typing import Tuple

# ML libs
import torch
import torch.neuron
from transformers import AutoModelForSequenceClassification

# 3rd party libraries
import pytest


@pytest.mark.core
@pytest.mark.compilation
def neuron_compile_torch_function_test(torch_function_input, test_output_dir) -> None:
    def foo(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return 2 * x + y

    # Run `foo` with the provided inputs and record the tensor operations
    traced_foo = torch.neuron.trace(foo, torch_function_input)
    # `traced_foo` can now be run with the TorchScript interpreter or saved
    # and loaded in a Python-free environment
    torch.jit.save(traced_foo, os.path.join(test_output_dir, "traced_foo.pt"))


@pytest.mark.inference
def neuron_inference_torch_function_test(test_output_dir, torch_function_input):

    traced_foo = torch.jit.load(os.path.join(test_output_dir, "traced_foo.pt"))
    traced_foo(*torch_function_input)


@pytest.mark.core
@pytest.mark.compilation
def neuron_compile_torch_graph_test(torch_graph_input, test_output_dir) -> None:
    class Net(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.conv = torch.nn.Conv2d(1, 1, 3)

        def forward(self, x: torch.Tensor) -> float:
            return self.conv(x) + 1

    n = Net()
    n.eval()
    # Trace a specific method and construct `ScriptModule` with
    # a single `forward` method
    neuron_forward = torch.neuron.trace(n.forward, torch_graph_input)
    torch.jit.save(neuron_forward, os.path.join(test_output_dir, "neuron_forward.pt"))
    # Trace a module (implicitly traces `forward`) and constructs a
    # `ScriptModule` with a single `forward` method
    neuron_net = torch.neuron.trace(n, torch_graph_input)
    torch.jit.save(neuron_net, os.path.join(test_output_dir, "neuron_net.pt"))


@pytest.mark.inference
def neuron_inference_torch_graph_test(test_output_dir, torch_graph_input):

    neuron_forward = torch.jit.load(os.path.join(test_output_dir, "neuron_forward.pt"))
    neuron_forward(torch_graph_input)

    neuron_net = torch.jit.load(os.path.join(test_output_dir, "neuron_net.pt"))
    neuron_net.forward(torch_graph_input)


@pytest.mark.core
@pytest.mark.compilation
def neuron_compile_transformer_nlp_model_test(
    torch_model_name: str,
    torch_model_input: Tuple[torch.Tensor, torch.Tensor],
    test_output_dir,
) -> None:

    model = AutoModelForSequenceClassification.from_pretrained(
        torch_model_name, torchscript=True
    )
    model.eval()

    model_neuron = torch.neuron.trace(model, torch_model_input)

    torch.jit.save(
        model_neuron,
        os.path.join(
            test_output_dir,
            "transformer_nlp_model_neuron.pt",
        ),
    )


@pytest.mark.inference
def neuron_inference_transformer_nlp_model_test(test_output_dir, torch_model_input):

    neuron_model_scripted = torch.jit.load(
        os.path.join(
            test_output_dir,
            "transformer_nlp_model_neuron.pt",
        )
    )

    neuron_model_scripted(*torch_model_input)
