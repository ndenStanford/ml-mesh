# 3rd party libraries
import pytest
from conftest import MODEL_MAX_LENGTH
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.ml_compile import CompiledTokenizer


@pytest.mark.parametrize(
    "tokenization_kwargs,expected_tokenization_settings",
    [
        (
            {"setting_1": "A", "setting_2": 10, "setting_3": True},
            {
                "setting_1": "A",
                "setting_2": 10,
                "setting_3": True,
                "padding": "max_length",
                "truncation": True,
                "add_special_tokens": True,
                "max_length": MODEL_MAX_LENGTH,
            },
        ),
        (
            lazy_fixture("custom_tokenization_settings"),
            lazy_fixture("custom_tokenization_settings"),
        ),
    ],
)
def compiled_tokenizer__from_tokenizer_test(
    mock_tokenizer,
    tokenization_kwargs,
    expected_tokenization_settings,
    all_delegated_method_references_with_sample_inputs,
):

    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=mock_tokenizer, **tokenization_kwargs
    )
    # --- validation suite: compiled tokenizer against passed mock tokenizer and expected ground
    # truths
    # validate tokenization settings
    assert compiled_tokenizer.tokenization_settings == expected_tokenization_settings

    # validate delegated tokenization methods
    for (
        delegated_method_reference,
        sample_input,
    ) in all_delegated_method_references_with_sample_inputs:
        assert getattr(compiled_tokenizer, delegated_method_reference)(
            sample_input
        ) == getattr(compiled_tokenizer.tokenizer, delegated_method_reference)(
            sample_input
        )
    # validate configured __call__ method
    tokenization___call___input = all_delegated_method_references_with_sample_inputs[0][
        1
    ]  # text string for tokenizer() call
    assert compiled_tokenizer(
        tokenization___call___input
    ) == compiled_tokenizer.tokenizer(
        tokenization___call___input, **compiled_tokenizer.tokenization_settings
    )
