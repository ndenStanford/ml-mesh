"""Test compiled tokenizer."""

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledTokenizer


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
def test_compiled_tokenizer_from_tokenizer(
    mock_tokenizer,
    tokenization_kwargs,
    expected_tokenization_settings,
):
    """Checks __init__ call and tokenizer settings value fallback logic."""
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
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
def test_compiled_tokenizer___call__(mock_tokenizer, tokenization_kwargs):
    """Checks tokenizer __call__ method."""
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )
    # validate configured __call__ method
    tokenization___call___input = "some example text"

    assert compiled_tokenizer(
        tokenization___call___input
    ) == compiled_tokenizer.tokenizer(
        tokenization___call___input, **compiled_tokenizer.tokenization_settings
    )
