from libs.keyword.onclusiveml.keyword.compile_pipeline import compile_pipeline
from keybert.backend._hftransformers import HFTransformerBackend
from keybert import KeyBERT
import numpy as np


def test_regression_compiled_hf_pipeline(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Regression testing:
    - a huggingface pipeline with pytorch model backend VS
    - a huggingface pipeline with a compiled (neuron) torchscript model backend
    
    For sequence below the test tokenizer max length of 300, the resulting
    embedding features should be the same."""

    # apply 'normal' pipeline, but make sure its using the same tokenization as the compiled
    # pipeline
    features = hf_feature_extraction_pipeline(
        test_documents, tokenize_kwargs=tokenizer_settings
    )

    compiled_pipeline = compile_pipeline(
        pipeline=hf_feature_extraction_pipeline,
        traced_model=traced_hf_feature_extraction_model,
        tokenizer_settings=tokenizer_settings,
    )

    compiled_features = compiled_pipeline(test_documents)
    
    # hf pipeline is outputting dynamically tokenized documents
    for embedded_document, compiled_embedded_document in zip(features, compiled_features):
        embedded_tokens, compiled_embedded_tokens = embedded_document[0], compiled_embedded_document[0]
        
        n_tokens = len(embedded_tokens)
        
        for token_index in range(n_tokens):
            embedded_token = embedded_tokens[token_index]
            compiled_token = compiled_embedded_tokens[token_index]

            np.testing.assert_almost_equal(embedded_token, compiled_token, decimal=4)


def test_regression_compiled_hfbackend(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Regression testing:
    - a keybert library HFTransformerBackend with a huggingface pipeline with pytorch model backend VS
    - a keybert library HFTransformerBackend with a huggingface pipeline with a compiled (neuron) torchscript model backend
    
    For sequence below the test tokenizer max length of 300, the resulting
    embedding features should be the same."""

    hf_keybert_backend = HFTransformerBackend(hf_feature_extraction_pipeline)
    embeddings = hf_keybert_backend.embed(test_documents)

    # keybert with torchscript model backend
    compiled_pipeline = compile_pipeline(
        pipeline=hf_feature_extraction_pipeline,
        traced_model=traced_hf_feature_extraction_model,
        tokenizer_settings=tokenizer_settings,
    )

    compiled_hf_pipeline_backend = HFTransformerBackend(
        embedding_model=compiled_pipeline
    )
    compiled_embeddings = compiled_hf_pipeline_backend.embed(test_documents)

    np.testing.assert_almost_equal(embeddings, compiled_embeddings)


def test_regression_compiled_keybert(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Regression testing:
    - a keybert library KeyBERT model using a HFTransformerBackend with a huggingface pipeline with pytorch model backend VS
    - a keybert library KeyBERT model using a HFTransformerBackend with a huggingface pipeline with a compiled (neuron) torchscript model backend
    
    For sequence below the test tokenizer max length of 300, the resulting
    embedding features should be the same."""

    keybert = KeyBERT(model=hf_feature_extraction_pipeline)
    keywords = keybert.extract_keywords(
        test_documents, keyphrase_ngram_range=(1, 1), stop_words=None
    )

    # keybert with torchscript model backend
    compiled_pipeline = compile_pipeline(
        pipeline=hf_feature_extraction_pipeline,
        traced_model=traced_hf_feature_extraction_model,
        tokenizer_settings=tokenizer_settings,
    )

    compiled_keybert = KeyBERT(model=compiled_pipeline)
    compiled_keywords = compiled_keybert.extract_keywords(
        test_documents, keyphrase_ngram_range=(1, 1), stop_words=None
    )

    assert keywords == compiled_keywords
