from libs.keyword.onclusiveml.keyword.compile_pipeline import compile_pipeline
from keybert.backend._hftransformers import HFTransformerBackend
from keybert import KeyBERT
import numpy as np


def test_scoring_compiled_hf_pipeline(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Tests the pipeline with torchscript model backend for executability"""

    compiled_pipeline = compile_pipeline(
        pipeline=hf_feature_extraction_pipeline,
        traced_model=traced_hf_feature_extraction_model,
        tokenizer_settings=tokenizer_settings,
    )

    compiled_pipeline(test_documents)


def test_regression_compiled_hf_pipeline(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Regression tests pipeline with torchscript model backend against 'normal' huggingface model
    backend pipeline. For sequence below the test tokenizer max length of 300, the resulting
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

    np.testing.assert_almost_equal(features, compiled_features)


def test_scoring_compiled_hfbackend(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Tests compatibility of compiled pipeline with the keybert libary's
    HFTransformerBackend class"""

    # keybert with torchscript model backend
    compiled_pipeline = compile_pipeline(
        pipeline=hf_feature_extraction_pipeline,
        traced_model=traced_hf_feature_extraction_model,
        tokenizer_settings=tokenizer_settings,
    )

    compiled_hf_pipeline_backend = HFTransformerBackend(
        embedding_model=compiled_pipeline
    )

    compiled_hf_pipeline_backend.embed(test_documents)


def test_regression_compiled_hfbackend(
    hf_feature_extraction_pipeline,
    traced_hf_feature_extraction_model,
    tokenizer_settings,
    test_documents,
):
    """Tests regression w.r.t a generic pipeline backend HFTransformerBackend
    instance"""

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
    """Tests compatibility of compiled pipeline with the customised
    HFTransformerBackend class"""

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
