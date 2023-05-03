# Standard Library
import shutil

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.keywords import CompiledKeyBERT


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)


@pytest.mark.order(2)
@pytest.mark.keybert
@pytest.mark.parametrize(
    "document_pipeline, compiled_word_pipeline",
    [
        (
            lazy_fixture("test_hf_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
        ),
        (
            lazy_fixture("test_compiled_document_pipeline"),
            lazy_fixture("test_compiled_word_pipeline"),
        ),
        (
            lazy_fixture("test_neuron_compiled_document_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
        ),
    ],
)
def compiled_keybert_extract_keywords_test(
    document_pipeline, compiled_word_pipeline, test_documents
):
    # either fully compiled keybert or a hybrid with document embedding pipeline uncompiled
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=document_pipeline,
        compiled_word_pipeline=compiled_word_pipeline,
    )

    test_compiled_keywords = compiled_keybert.extract_keywords(docs=test_documents)

    assert len(test_compiled_keywords) == len(test_documents)
    assert all(
        [len(test_keywords_i) == 5 for test_keywords_i in test_compiled_keywords]
    )


@pytest.mark.order(2)
@pytest.mark.keybert
@pytest.mark.parametrize(
    "document_pipeline, compiled_word_pipeline",
    [
        (lazy_fixture("test_hf_pipeline"), lazy_fixture("test_compiled_word_pipeline")),
        (
            lazy_fixture("test_compiled_document_pipeline"),
            lazy_fixture("test_compiled_word_pipeline"),
        ),
        (
            lazy_fixture("test_neuron_compiled_document_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
        ),
    ],
)
def compiled_keybert_extract_embeddings_test(
    document_pipeline, compiled_word_pipeline, test_documents
):

    compiled_keybert = CompiledKeyBERT(
        document_pipeline=document_pipeline,
        compiled_word_pipeline=compiled_word_pipeline,
    )

    (
        test_document_embeddings,
        test_keyword_embeddings,
    ) = compiled_keybert.extract_embeddings(docs=test_documents)

    assert len(test_document_embeddings) == len(test_documents)
    assert (
        len(test_keyword_embeddings) >= 50
    )  # ~ 149 during testing, but not really deterministic


@pytest.mark.parametrize(
    "document_pipeline, compiled_word_pipeline",
    [
        (lazy_fixture("test_hf_pipeline"), lazy_fixture("test_compiled_word_pipeline")),
        (
            lazy_fixture("test_compiled_document_pipeline"),
            lazy_fixture("test_compiled_word_pipeline"),
        ),
        (
            lazy_fixture("test_neuron_compiled_document_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
        ),
    ],
)
def compiled_keybert_save_pretrained_from_pretrained(
    document_pipeline, compiled_word_pipeline, test_documents
):
    # initialize with constructor and score
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=document_pipeline,
        compiled_word_pipeline=compiled_word_pipeline,
    )

    test_compiled_keywords = compiled_keybert.extract_keywords(docs=test_documents)

    # save, load and score again
    compiled_keybert.save_pretrained("./test")
    compiled_keybert_reloaded = CompiledKeyBERT.from_pretrained("./test")

    test_compiled_keywords_reloaded = compiled_keybert_reloaded.extract_keywords(
        docs=test_documents
    )

    assert test_compiled_keywords == test_compiled_keywords_reloaded
    # clean up
    shutil.rmtree("./test")
