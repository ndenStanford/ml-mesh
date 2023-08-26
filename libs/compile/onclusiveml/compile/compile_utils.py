"""Compilation helper classes."""

# Internal libraries
from onclusiveml.core.base import OnclusiveEnum


class DelegatedTokenizerMethods(OnclusiveEnum):
    """Delegated tokenizer methods."""

    encode_plus: str = "encode_plus"
    encode: str = "encode"
    decode: str = "decode"
    create_token_type_ids_from_sequences: str = "create_token_type_ids_from_sequences"
    convert_ids_to_tokens: str = "convert_ids_to_tokens"
    convert_tokens_to_string: str = "convert_tokens_to_string"
    clean_up_tokenization: str = "clean_up_tokenization"


class DelegatedTokenizerAttributes(OnclusiveEnum):
    """Delegated tokenizer attributes."""

    is_fast: str = "is_fast"
    _tokenizer: str = "_tokenizer"
    unk_token_id: str = "unk_token_id"


class DelegatedPipelineAttributes(OnclusiveEnum):
    """Delegated pipeline attributes."""

    tokenizer: str = "tokenizer"
    model: str = "model"
