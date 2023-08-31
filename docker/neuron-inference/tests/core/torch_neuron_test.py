"""Torch neuron test."""

# Standard Library
import os

# ML libs
import torch
import torch.neuron

# 3rd party libraries
import pytest


@pytest.mark.inference
def test_neuron_inference_torch_function(test_output_dir, torch_function_input):
    """Test neuron torch function."""
    traced_foo = torch.jit.load(
        os.path.join(test_output_dir, "compiled_torch_function.pt")
    )
    traced_foo(*torch_function_input)


@pytest.mark.inference
def test_neuron_inference_torch_graph(test_output_dir, torch_graph_input):
    """Test neuron inference torch graph."""
    neuron_forward = torch.jit.load(
        os.path.join(test_output_dir, "compiled_torch_forward_pass.pt")
    )
    neuron_forward(torch_graph_input)

    neuron_net = torch.jit.load(os.path.join(test_output_dir, "compiled_torch_net.pt"))
    neuron_net.forward(torch_graph_input)


@pytest.mark.inference
def test_neuron_inference_transformer_nlp_model(test_output_dir, torch_model_input):
    """Test neuron inference transformer nlp model."""
    neuron_model_scripted = torch.jit.load(
        os.path.join(
            test_output_dir,
            "compiled_transformer_nlp_model.pt",
        )
    )

    neuron_model_scripted(*torch_model_input)
