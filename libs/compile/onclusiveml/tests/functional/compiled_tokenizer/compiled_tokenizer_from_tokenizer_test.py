# Standard Library
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
    # --- validation suite: compiled tokenizer against passed mock tokenizer and expected ground
    # truths
    # for ground truth, set the only tokenization settings value that depends on the huggingface
    # reference model
    if "max_length" not in tokenization_kwargs:
        expected_tokenization_settings["max_length"] = huggingface_model_max_length
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings
    # validate delegated tokenization methods
    for (
        delegated_method_reference,
        sample_input,
    ) in all_delegated_method_references_with_sample_inputs:
        assert getattr(compiled_tokenizer, delegated_method_reference)(
            sample_input
        ) == getattr(huggingface_tokenizer, delegated_method_reference)(sample_input)
    # validate configured __call__ method
    # list outputs
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][
        1
    ]  # text string for tokenizer() call
    list_compiled_tokenizer_output: Dict[str, List] = compiled_tokenizer(
        tokenization___call___input
    )
    list_huggingface_tokenizer_output: Dict[str, List] = huggingface_tokenizer(
        tokenization___call___input, **compiled_tokenizer.tokenization_settings
    )
    assert list_compiled_tokenizer_output == list_huggingface_tokenizer_output
    # torch outputs
    torch_compiled_tokenizer_output: Dict[str, torch.Tensor] = compiled_tokenizer(
        tokenization___call___input, return_tensors="pt"
    )
    torch_huggingface_tokenizer_output: Dict[str, torch.Tensor] = huggingface_tokenizer(
        tokenization___call___input,
        return_tensors="pt",
        **compiled_tokenizer.tokenization_settings
    )

    for token_type in torch_huggingface_tokenizer_output:
        torch.testing.assert_close(
            torch_huggingface_tokenizer_output[token_type],
            torch_compiled_tokenizer_output[token_type],
        )
