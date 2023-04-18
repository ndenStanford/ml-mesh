# Standard Library
import base64
import os
import pickle
from typing import List

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.ml_compile import CompiledTokenizer


MODEL_MAX_LENGTH = 50

@pytest.fixture
def input_tokenization_settings():
    
    return {
                "setting_1": "A",
                "setting_2": 10,
                "setting_3": True,
                "padding": "max_length",
                "truncation": True,
                "add_special_tokens": True,
                "max_length": MODEL_MAX_LENGTH,
            }
    
class MockTokenizer(object):
    """Dummy tokenizer class to help validate attribute and method referencing functionality of
    the CompiledTokenizer class. Mock attributes and methods include:
    - model_max_length (att)
    - encode_plus (m)
    - encode (m)
    - decode (m)
    - create_token_type_ids_from_sequences (m)
    - convert_tokens_to_string (m)
    - clean_up_tokenization (m)
    - __call__ (m)
    - save_pretrained (m)
    - from_pretrained (m)"""

    def __init__(self):
        self.model_max_length = MODEL_MAX_LENGTH

    def encode_plus(self, text: str):

        return base64.b64encode((text + "_encoded").encode("utf-8"))

    def encode(self, text: str):

        return base64.b64encode(text.encode("utf-8"))

    def decode(self, encoded_text: bytes):

        return base64.b64decode(encoded_text).decode("utf-8")

    def create_token_type_ids_from_sequences(self, tokens: List[str]):

        return [
            0,
        ] * len(tokens)

    def convert_tokens_to_string(self, tokens: List[int]):

        return " ".join(str(tokens))

    def clean_up_tokenization(self, text: str):

        return text.replace(" .", "").replace(" ,", ",")

    def __call__(self, text: str, padding: str = None, **kwargs):

        split_text = text.split(" ")

        tokens = [i for i in range(len(split_text))]
        # simulate very basic max_length logic for non-trivial validations
        if padding == "max_length":
            tokens = tokens + [
                0,
            ] * (self.model_max_length - len(tokens))

        return tokens

    def save_pretrained(self, directory):

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(os.path.join(directory, "mock_tokenizer.pkl"), "wb") as mock_file:
            pickle.dump(self, mock_file)

    @classmethod
    def from_pretrained(cls, directory):

        with open(os.path.join(directory, "mock_tokenizer.pkl"), "rb") as mock_file:
            mock_tokenizer = pickle.load(mock_file)

        return mock_tokenizer


@pytest.fixture
def mock_tokenizer():

    return MockTokenizer()


@pytest.fixture
def custom_tokenization_settings():

    return {
        "setting_1": "A",
        "setting_2": 10,
        "setting_3": True,
        "padding": "some value",
        "truncation": False,
        "add_special_tokens": False,
        "max_length": 20,
    }


@pytest.fixture
def compiled_tokenizer(custom_tokenization_settings):

    return CompiledTokenizer.from_tokenizer(
        tokenizer=MockTokenizer(), **custom_tokenization_settings
    )


@pytest.fixture
def all_delegated_method_references_with_sample_inputs():

    return (
        ("encode_plus", "some example text"),
        ("encode", "some example text"),
        ("decode", base64.b64encode("some example text".encode("utf-8"))),
        ("create_token_type_ids_from_sequences", ["some", "example", "text"]),
        ("convert_tokens_to_string", [0, 1, 2]),
        ("clean_up_tokenization", "some ,example text ."),
    )
