"""Compiled model tokenizer initialization test."""

# Standard Library
import base64

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledTokenizer
from onclusiveml.compile.compile_utils import (
    DelegatedTokenizerAttributes,
    DelegatedTokenizerMethods,
)


@pytest.mark.parametrize(
    "tokenization_kwargs,expected_tokenization_settings",
    [
        (
            {"setting_1": "A", "setting_2": 10, "setting_3": True},
            lazy_fixture("input_tokenization_settings"),
        ),
        (
            lazy_fixture("custom_tokenization_settings"),
            lazy_fixture("custom_tokenization_settings"),
        ),
    ],
)
def test_compiled_tokenizer___init(
    mock_tokenizer,
    tokenization_kwargs,
    expected_tokenization_settings,
):
    """Checks __init__ call and tokenizer settings value fallback logic."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings


@pytest.mark.parametrize(
    "tokenization_kwargs",
    [
        {"setting_1": "A", "setting_2": 10, "setting_3": True},
        lazy_fixture("custom_tokenization_settings"),
    ],
)
def test_compiled_tokenizer___call__(
    mock_tokenizer,
    tokenization_kwargs,
):
    """Checks tokenizer __call__ method."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )
    # validate configured __call__ method
    tokenization___call___input = "some example text"

    assert compiled_tokenizer(
        tokenization___call___input
    ) == compiled_tokenizer.tokenizer(
        tokenization___call___input, **compiled_tokenizer.tokenization_settings
    )


@pytest.mark.parametrize(
    "tokenization_kwargs",
    [
        {"setting_1": "A", "setting_2": 10, "setting_3": True},
        lazy_fixture("custom_tokenization_settings"),
    ],
)
@pytest.mark.parametrize(
    "delegated_tokenizer_method, method_input",
    [
        (DelegatedTokenizerMethods.encode_plus.value, "some example text"),
        (DelegatedTokenizerMethods.encode.value, "some example text"),
        (
            DelegatedTokenizerMethods.decode.value,
            base64.b64encode("some example text".encode("utf-8")),
        ),
        (
            DelegatedTokenizerMethods.create_token_type_ids_from_sequences.value,
            ["some", "example", "text"],
        ),
        (DelegatedTokenizerMethods.convert_ids_to_tokens.value, [1, 2, 3]),
        (DelegatedTokenizerMethods.convert_tokens_to_string.value, [0, 1, 2]),
        (DelegatedTokenizerMethods.clean_up_tokenization.value, "some ,example text ."),
    ],
)
def test_compiled_tokenizer_delegated_methods(
    mock_tokenizer, tokenization_kwargs, delegated_tokenizer_method, method_input
):
    """Checks all delegated tokenizer methods."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )

    assert getattr(compiled_tokenizer, delegated_tokenizer_method)(
        method_input
    ) == getattr(compiled_tokenizer.tokenizer, delegated_tokenizer_method)(method_input)


@pytest.mark.parametrize(
    "tokenization_kwargs",
    [
        {"setting_1": "A", "setting_2": 10, "setting_3": True},
        lazy_fixture("custom_tokenization_settings"),
    ],
)
@pytest.mark.parametrize(
    "delegated_tokenizer_attribute",
    [
        DelegatedTokenizerAttributes.is_fast.value,
        DelegatedTokenizerAttributes._tokenizer.value,
        DelegatedTokenizerAttributes.unk_token_id.value,
    ],
)
def test_compiled_tokenizer_delegated_attributes(
    mock_tokenizer, tokenization_kwargs, delegated_tokenizer_attribute
):
    """Checks all delegated tokenizer attributes."""
    compiled_tokenizer = CompiledTokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )

    assert getattr(compiled_tokenizer, delegated_tokenizer_attribute) == getattr(
        compiled_tokenizer.tokenizer, delegated_tokenizer_attribute
    )
