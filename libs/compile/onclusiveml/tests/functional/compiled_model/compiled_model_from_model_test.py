# ML libs
import torch
import torch.neuron

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledModel


@pytest.mark.parametrize(
    "huggingface_model_reference, sample_inputs",
    [
        # 'prajjwal1/bert-tiny',
        (
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            lazy_fixture("test_inputs"),
        ),
        ("dslim/bert-base-NER", lazy_fixture("test_ner_inputs")),
    ],
)
@pytest.mark.parametrize("neuron", [True, False])  # regular torchscript
@pytest.mark.parametrize("batch_size", [1, 2, 4])
@pytest.mark.parametrize(
    "max_length",
    [
        35,
        # None, # for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', this is 512
        # and takes a long time for neuron tracing
    ],
)
def test_compiled_model_from_model(
    huggingface_tokenizer,
    huggingface_model,
    batch_size,
    max_length,
    neuron,
    sample_inputs,
    regression_test_atol,
    regression_test_rtol,
):
    # compile model including built-in validation on tracing inputs
    kwargs = {
        "batch_size": batch_size,
        "max_length": max_length,
        "neuron": neuron,
    }

    compiled_model = CompiledModel.from_model(
        model=huggingface_model,
        validate_compilation=True,
        validation_atol=regression_test_atol,
        validation_rtol=regression_test_rtol,
        **kwargs
    )
    # additional, regression based validation with custom tokenizer & inputs
    sample_tokens = huggingface_tokenizer(
        sample_inputs,
        return_tensors="pt",
        max_length=max_length,
        padding="max_length",
        truncation=True,
    )
    huggingface_model_output = huggingface_model(**sample_tokens)
    compiled_model_output = compiled_model(**sample_tokens)

    torch.testing.assert_close(
        huggingface_model_output[0],  # ignore gradient at position 1
        compiled_model_output[0],
        atol=0.05,
        rtol=0.05,
    )
