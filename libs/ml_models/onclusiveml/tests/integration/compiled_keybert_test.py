# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.ml_models.keywords import CompiledKeyBERT


@pytest.mark.order(2)
@pytest.mark.keybert
@pytest.mark.parametrize(
    "compiled_word_pipeline, compiled_document_pipeline",
    [
        (
            lazy_fixture("test_compiled_word_pipeline"),
            lazy_fixture("test_compiled_document_pipeline"),
        ),
        (
            lazy_fixture("test_neuron_compiled_word_pipeline"),
            lazy_fixture("test_neuron_compiled_document_pipeline"),
        ),
    ],
)
def compiled_keybert_extract_keywords_test(
    compiled_word_pipeline, compiled_document_pipeline, test_documents
):

    compiled_keybert = CompiledKeyBERT(
        compiled_word_pipeline=compiled_word_pipeline,
        compiled_document_pipeline=compiled_document_pipeline,
    )

    test_keywords = compiled_keybert.extract_keywords(docs=test_documents)

    assert len(test_keywords) == len(test_documents)
    assert all([len(test_keywords_i) == 5 for test_keywords_i in test_keywords])


@pytest.mark.order(2)
@pytest.mark.keybert
@pytest.mark.parametrize(
    "compiled_word_pipeline, compiled_document_pipeline",
    [
        (
            lazy_fixture("test_compiled_word_pipeline"),
            lazy_fixture("test_compiled_document_pipeline"),
        ),
        (
            lazy_fixture("test_neuron_compiled_word_pipeline"),
            lazy_fixture("test_neuron_compiled_document_pipeline"),
        ),
    ],
)
def compiled_keybert_extract_embeddings_test(
    compiled_word_pipeline, compiled_document_pipeline, test_documents
):

    compiled_keybert = CompiledKeyBERT(
        compiled_word_pipeline=compiled_word_pipeline,
        compiled_document_pipeline=compiled_document_pipeline,
    )

    (
        test_document_embeddings,
        test_keyword_embeddings,
    ) = compiled_keybert.extract_embeddings(docs=test_documents)

    assert len(test_document_embeddings) == len(test_documents)
    assert (
        len(test_keyword_embeddings) >= 50
    )  # ~ 149 during testing, but not really deterministic
