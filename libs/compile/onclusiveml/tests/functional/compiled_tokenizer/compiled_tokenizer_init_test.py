"""Compiled tokenizer initialisation test."""

# ML libs
import torch

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledTokenizer


@pytest.mark.parametrize(
    "huggingface_model_reference",
    [
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "dslim/bert-base-NER",
    ],
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
):
    """Checks __init__ call and tokenizer settings value fallback logic."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=huggingface_tokenizer, **tokenization_kwargs
    )

    if "max_length" not in tokenization_kwargs:
        expected_tokenization_settings["max_length"] = huggingface_model_max_length
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings


@pytest.mark.parametrize(
    "huggingface_model_reference",
    [
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "dslim/bert-base-NER",
    ],
)
@pytest.mark.parametrize(
    "tokenization_kwargs",
    [
        {},
        lazy_fixture("custom_tokenization_settings_1"),
        lazy_fixture("custom_tokenization_settings_2"),
        lazy_fixture("custom_tokenization_settings_3"),
    ],
)
@pytest.mark.parametrize(
    "return_tensors",
    [
        "pt",
        None,
    ],
)
def test_compiled_tokenizer___call__(
    huggingface_tokenizer, tokenization_kwargs, return_tensors
):
    """Checks tokenizer __call__ method."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=huggingface_tokenizer, **tokenization_kwargs
    )
    # validate configured __call__ method
    tokenization___call___input = "some example text"

    compiled_tokenizer_output = compiled_tokenizer(
        tokenization___call___input, return_tensors=return_tensors
    )

    huggingface_tokenizer_output = compiled_tokenizer.tokenizer(
        tokenization___call___input,
        return_tensors=return_tensors,
        **compiled_tokenizer.tokenization_settings,
    )

    if return_tensors == "pt":
        for token_type in huggingface_tokenizer_output:
            torch.testing.assert_close(
                huggingface_tokenizer_output[token_type],
                compiled_tokenizer_output[token_type],
            )
    else:
        assert huggingface_tokenizer_output == compiled_tokenizer_output
