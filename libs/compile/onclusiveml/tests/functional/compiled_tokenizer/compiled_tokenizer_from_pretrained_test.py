# Standard Library
import shutil

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
    "tokenization_kwargs",
    [
        {},
        lazy_fixture("custom_tokenization_settings_1"),
        lazy_fixture("custom_tokenization_settings_2"),
        lazy_fixture("custom_tokenization_settings_3"),
    ],
)
def test_compiled_tokenizer_from_pretrained(
    huggingface_tokenizer,
    tokenization_kwargs,
):
    """Checks __init__ call and tokenizer settings value fallback logic"""

    compiled_tokenizer = CompiledTokenizer.from_tokenizer(
        tokenizer=huggingface_tokenizer, **tokenization_kwargs
    )

    compiled_tokenizer.save_pretrained("test_compiled_tokenizer")
    reloaded_compiled_tokenizer = compiled_tokenizer.from_pretrained(
        "test_compiled_tokenizer"
    )
    # validate tokenization settings
    assert (
        compiled_tokenizer.tokenization_settings
        == reloaded_compiled_tokenizer.tokenization_settings  # noqa: W503
    )
    # clean up local dir
    shutil.rmtree("test_compiled_tokenizer")
