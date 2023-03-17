import os
import pytest
import torch
import torch.neuron
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import List


@pytest.mark.core
def test_neuron_compile_torch_function() -> None:
    def foo(x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        return 2 * x + y

    inputs = (torch.rand(3), torch.rand(3))

    # Run `foo` with the provided inputs and record the tensor operations
    traced_foo = torch.neuron.trace(foo, inputs)

    # `traced_foo` can now be run with the TorchScript interpreter or saved
    # and loaded in a Python-free environment
    torch.jit.save(traced_foo, os.path.join("./output", "traced_foo.pt"))


@pytest.mark.core
def test_neuron_compile_torch_graph() -> None:
    class Net(torch.nn.Module):
        def __init__(self) -> None:
            super(Net, self).__init__()
            self.conv = torch.nn.Conv2d(1, 1, 3)

        def forward(self, x: torch.Tensor) -> float:
            return self.conv(x) + 1

    n = Net()
    n.eval()

    inputs = torch.rand(1, 1, 3, 3)

    # Trace a specific method and construct `ScriptModule` with
    # a single `forward` method
    neuron_forward = torch.neuron.trace(n.forward, inputs)
    torch.jit.save(neuron_forward, os.path.join("./output", "neuron_forward.pt"))

    # Trace a module (implicitly traces `forward`) and constructs a
    # `ScriptModule` with a single `forward` method
    neuron_net = torch.neuron.trace(n, inputs)
    torch.jit.save(neuron_net, os.path.join("./output", "neuron_net.pt"))


@pytest.mark.core
@pytest.mark.parametrize(
    "model_name, dynamic_batch_size",
    [
        ("distilbert-base-uncased-finetuned-sst-2-english", False),
        ("distilbert-base-uncased-finetuned-sst-2-english", True),
    ],
)
def test_neuron_compile_transformer_nlp_model(
    model_name: str,
    text_tracing_input: List[str],
    dynamic_batch_size: bool,
    max_length: int,
) -> None:

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, torchscript=True
    )
    model.eval()

    tokens = tokenizer(
        text_tracing_input,
        add_special_tokens=True,
        padding="max_length",
        max_length=max_length,
        truncation=True,
        return_tensors="pt",
    )

    token_tracing_input = tokens["input_ids"], tokens["attention_mask"]

    model_neuron = torch.neuron.trace(
        model, token_tracing_input, dynamic_batch_size=dynamic_batch_size
    )

    torch.jit.save(
        model_neuron,
        os.path.join(
            "./output",
            f"transformer_nlp_model_neuron_{model_name}_{dynamic_batch_size}.pt",
        ),
    )


@pytest.mark.extended
@pytest.mark.parametrize(
    "model_name, dynamic_batch_size", [("resnet50", False), ("resnet50", True)]
)
def test_neuron_compile_torch_vision_model(
    model_name: str, image_tracing_input: torch.Tensor, dynamic_batch_size: bool
) -> None:

    # Load the model and set it to evaluation mode
    model = torch.hub.load("pytorch/vision", model_name, pretrained=True)
    model.eval()

    # Compile with an example input of batch size 1
    model_neuron = torch.neuron.trace(
        model, image_tracing_input, dynamic_batch_size=dynamic_batch_size
    )

    torch.jit.save(
        model_neuron,
        os.path.join("./output", f"torch_vision_model_neuron_{dynamic_batch_size}.pt"),
    )


@pytest.mark.extended
@pytest.mark.parametrize(
    "model_name, model_head, dynamic_batch_size",
    [("bert-base-uncased", "model", False), ("bert-base-uncased", "model", True)],
)
def test_neuron_compile_torch_nlp_model(
    model_name: str,
    model_head: str,
    text_tracing_input: List[str],
    dynamic_batch_size: bool,
    max_length: int,
) -> None:

    tokenizer = torch.hub.load(
        "huggingface/pytorch-transformers", "tokenizer", model_name
    )
    model = torch.hub.load(
        "huggingface/pytorch-transformers",
        model_head,
        model_name,
        torchscript=True,
    )
    model.eval()

    tokens = tokenizer(
        text_tracing_input,
        add_special_tokens=True,
        padding="max_length",
        max_length=max_length,
        truncation=True,
        return_tensors="pt",
    )

    token_tracing_input = tokens["input_ids"], tokens["attention_mask"]

    # neuron trace model
    neuron_model = torch.neuron.trace(
        model, token_tracing_input, dynamic_batch_size=dynamic_batch_size
    )

    # export neuron traced model
    torch.jit.save(
        neuron_model,
        os.path.join(
            "./output",
            f"torch_nlp_model_neuron_{model_name}_{model_head}_{dynamic_batch_size}.pt",
        ),
    )