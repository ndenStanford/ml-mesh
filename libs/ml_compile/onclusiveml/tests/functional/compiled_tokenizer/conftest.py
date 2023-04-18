# ML libs
from transformers import AutoTokenizer

# 3rd party libraries
import pytest


MODEL_MAX_LENGTH = 50


@pytest.fixture
def huggingface_tokenizer(huggingface_model_reference: str):

    return AutoTokenizer.from_pretrained(huggingface_model_reference)


@pytest.fixture
def huggingface_model_max_length(huggingface_tokenizer):

    return huggingface_tokenizer.model_max_length


@pytest.fixture
def custom_tokenization_settings_1():

    return {
        "padding": "longest",
        "truncation": False,
        "add_special_tokens": False,
        "max_length": 20,
    }


@pytest.fixture
def custom_tokenization_settings_2():

    return {
        "padding": "max_length",
        "truncation": True,
        "add_special_tokens": True,
        "max_length": 100,
    }


@pytest.fixture
def custom_tokenization_settings_3():

    return {
        "padding": "do_not_pad",
        "truncation": False,
        "add_special_tokens": False,
        "max_length": 200,
    }


@pytest.fixture
def all_delegated_method_references_with_sample_inputs():

    return (
        (
            "encode_plus",
            """This is some example text to tokenize. It is used to regression test the compiled
            tokenizer.""",
        ),
        (
            "encode",
            """This is some example text to tokenize. It is used to regression test the compiled
            tokenizer.""",
        ),
        # ('decode',None),
        ("create_token_type_ids_from_sequences", ["some", "example", "text"]),
        # ('convert_tokens_to_string',[0,1,2]),
        ("clean_up_tokenization", "some ,example text ."),
    )
