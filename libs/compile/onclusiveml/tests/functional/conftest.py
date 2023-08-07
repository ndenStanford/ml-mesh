# Standard Library
from typing import List

# ML libs
from transformers import AutoModel, AutoTokenizer
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile.compile_utils import (
    DelegatedPipelineAttributes,
    DelegatedTokenizerAttributes,
    DelegatedTokenizerMethods,
)


@pytest.fixture
def test_inputs() -> List[str]:

    return (
        [
            "This is an extremely bad and short sample input.",
            "This is a pretty neutral sentence."
            """This is another, much, much better sample input. It is amazing! This is to test how
        the compiled model handles more than one tokenized sample at a time.""",
        ]
        * 2  # noqa: W503
    )


@pytest.fixture
def test_ner_inputs() -> List[str]:

    return [
        "My name is Sebastian, I live in London, which is a city in the United Kingdom.",
        "Yesterday I went to Kew Gardens, a public garden in the county of Surrey.",
        "Sherlock Holmes is a brilliant detective in England. Watson is his able assistent.",
    ]


@pytest.fixture
def huggingface_tokenizer(huggingface_model_reference: str):

    return AutoTokenizer.from_pretrained(huggingface_model_reference)


@pytest.fixture
def huggingface_model_max_length(huggingface_tokenizer):

    return huggingface_tokenizer.model_max_length


@pytest.fixture
def regression_test_atol():
    return 2.5e-02


@pytest.fixture
def regression_test_rtol():
    return 1e-02


# ---------- compiled tokenizer
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
def delegated_tokenizer_methods_w_input():

    return (
        (
            DelegatedTokenizerMethods.encode_plus.value,
            """This is some example text to tokenize. It is used to regression test the compiled
            tokenizer.""",
        ),
        (
            DelegatedTokenizerMethods.encode.value,
            """This is some example text to tokenize. It is used to regression test the compiled
            tokenizer.""",
        ),
        (
            DelegatedTokenizerMethods.create_token_type_ids_from_sequences.value,
            ["some", "example", "text"],
        ),
        (DelegatedTokenizerMethods.convert_ids_to_tokens.value, [1, 2, 3]),
        (DelegatedTokenizerMethods.clean_up_tokenization.value, "some ,example text ."),
    )


@pytest.fixture
def delegated_tokenizer_attributes():

    return (
        DelegatedTokenizerAttributes.is_fast.value,
        DelegatedTokenizerAttributes._tokenizer.value,
        DelegatedTokenizerAttributes.unk_token_id.value,
    )


# ---------- compiled model
@pytest.fixture
def huggingface_model(huggingface_model_reference: str):

    return AutoModel.from_pretrained(huggingface_model_reference)


# -------------- compiled pipeline
@pytest.fixture
def huggingface_pipeline(
    huggingface_pipeline_task: str, huggingface_model_reference: str
):

    return pipeline(task=huggingface_pipeline_task, model=huggingface_model_reference)


@pytest.fixture
def delegated_pipeline_attributes():

    return (
        DelegatedPipelineAttributes.tokenizer.value,
        DelegatedPipelineAttributes.model.value,
    )
