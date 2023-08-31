"""Compiled tokenizer from tokenizer test."""

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.compile import CompiledTokenizer


@pytest.mark.parametrize(
    "huggingface_model_reference",
    [
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "cardiffnlp/twitter-xlm-roberta-base-sentiment",
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
def test_compiled_tokenizer_from_tokenizer(
    huggingface_tokenizer,
    tokenization_kwargs,
    expected_tokenization_settings,
    huggingface_model_max_length,
):
    """Checks __init__ call and tokenizer settings value fallback logic."""
    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=huggingface_tokenizer, **tokenization_kwargs
    )

    if "max_length" not in tokenization_kwargs:
        expected_tokenization_settings["max_length"] = huggingface_model_max_length
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings
