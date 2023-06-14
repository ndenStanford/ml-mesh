# Standard Library
import shutil
from typing import Dict, List

# ML libs
import torch

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledTokenizer


@pytest.mark.parametrize(
    "huggingface_model_reference",
    ["sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"],
)
@pytest.mark.parametrize(
    "tokenization_kwargs,expected_tokenization_settings",
    [
        (
            {},
            {
                "padding": "max_length",
                "truncation": True,
                "add_special_tokens": True,
            },  # max_length is set inside the test
        ),
        (
            lazy_fixture("custom_tokenization_settings_1"),
            lazy_fixture("custom_tokenization_settings_1"),
        ),
        (
            lazy_fixture("custom_tokenization_settings_2"),
            lazy_fixture("custom_tokenization_settings_2"),
        ),
        (
            lazy_fixture("custom_tokenization_settings_3"),
            lazy_fixture("custom_tokenization_settings_3"),
        ),
    ],
)
def test_compiled_tokenizer__init(
    huggingface_tokenizer,
    tokenization_kwargs,
    expected_tokenization_settings,
    huggingface_model_max_length,
    all_delegated_method_references_with_sample_inputs,
):

    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=huggingface_tokenizer, **tokenization_kwargs
    )

    compiled_tokenizer.save_pretrained("test_compiled_tokenizer")
    reloaded_compiled_tokenizer = compiled_tokenizer.from_pretrained(
        "test_compiled_tokenizer"
    )
    # --- validation suite: reloaded compiled tokenizer against original compiled tokenizer
    # for ground truth, set the only tokenization settings value that depends on the huggingface
    # reference model
    if "max_length" not in tokenization_kwargs:
        expected_tokenization_settings["max_length"] = huggingface_model_max_length
    # validate tokenization settings
    assert (
        reloaded_compiled_tokenizer.tokenization_settings
        == compiled_tokenizer.tokenization_settings  # noqa: W503
    )
    # validate delegated tokenization methods of reloaded compiled tokenizer against equivalent
    # methods of original compiled tokenizer
    for (
        delegated_method_reference,
        sample_input,
    ) in all_delegated_method_references_with_sample_inputs:
        assert getattr(reloaded_compiled_tokenizer, delegated_method_reference)(
            sample_input
        ) == getattr(compiled_tokenizer, delegated_method_reference)(sample_input)
    # validate configured __call__ method of reloaded compiled tokenizer against original compiled
    # tokenizer's __call__ method
    # list outputs
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][
        1
    ]  # text string for tokenizer() call
    list_compiled_tokenizer_output: Dict[str, List] = compiled_tokenizer(
        tokenization___call___input
    )
    list_reloaded_compiled_tokenizer_output: Dict[
        str, List
    ] = reloaded_compiled_tokenizer(tokenization___call___input)
    assert list_compiled_tokenizer_output == list_reloaded_compiled_tokenizer_output
    # torch outputs
    torch_compiled_tokenizer_output: Dict[str, torch.Tensor] = compiled_tokenizer(
        tokenization___call___input, return_tensors="pt"
    )
    torch_reloaded_compiled_tokenizer_output: Dict[
        str, torch.Tensor
    ] = reloaded_compiled_tokenizer(tokenization___call___input, return_tensors="pt")

    for token_type in torch_compiled_tokenizer_output:
        torch.testing.assert_close(
            torch_reloaded_compiled_tokenizer_output[token_type],
            torch_compiled_tokenizer_output[token_type],
        )
    # clean up local dir
    shutil.rmtree("test_compiled_tokenizer")
