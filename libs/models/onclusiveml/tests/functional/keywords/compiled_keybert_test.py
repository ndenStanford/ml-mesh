"""Keywords."""

# Standard Library
import time

# ML libs
from keybert import KeyBERT

# 3rd party libraries
import pandas as pd
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.keywords import CompiledKeyBERT


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)


@pytest.mark.order(2)
@pytest.mark.regression
@pytest.mark.parametrize("document_index", [0, 1, 2])
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
def test_compiled_keybert_extract_keywords_regression(
    document_pipeline,
    compiled_word_pipeline,
    test_hf_pipeline,
    test_document,
    document_index,
):
    """Test compiled Keybert."""
    # compiled keybert
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=document_pipeline,
        compiled_word_pipeline=compiled_word_pipeline,
    )

    keywords_actual = compiled_keybert.extract_keywords(docs=test_document)[0]
    keywords_actual_df = pd.DataFrame(keywords_actual, columns=["keyword", "score"])

    # generic keybert - ground truth behaviour
    keybert = KeyBERT(model=test_hf_pipeline)

    keywords_expected = keybert.extract_keywords(docs=test_document)
    keywords_expected_df = pd.DataFrame(keywords_expected, columns=["keyword", "score"])

    # assert keywords are identical and scores are within 0.01 absolute deviation
    pd.testing.assert_frame_equal(keywords_actual_df, keywords_expected_df, atol=0.01)


@pytest.mark.order(2)
@pytest.mark.latency
@pytest.mark.parametrize(
    "keybert_scenario, document_pipeline, compiled_word_pipeline, n_runs, expected_speedup_factor",
    [
        (
            "hybrid",
            lazy_fixture("test_hf_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
            50,
            1.9,
        ),
        (
            "full-compiled",
            lazy_fixture("test_neuron_compiled_document_pipeline"),
            lazy_fixture("test_neuron_compiled_word_pipeline"),
            50,
            2.2,
        ),
    ],
)
def test_compiled_keybert_extract_keywords_latency(
    keybert_scenario,
    document_pipeline,
    compiled_word_pipeline,
    test_hf_pipeline,
    test_documents,
    n_runs,
    expected_speedup_factor,
):
    """Test compile keybert extract keywords latency."""
    # time compiled/hybrid keybert
    compiled_keybert = CompiledKeyBERT(
        document_pipeline=document_pipeline,
        compiled_word_pipeline=compiled_word_pipeline,
    )

    compiled_start = time.time()
    for i in range(n_runs):
        compiled_keybert.extract_keywords(test_documents)
    average_compiled_duration = (time.time() - compiled_start) / n_runs
    logger.info(f"Average {keybert_scenario} compiled keybert inference duration: ")
    logger.info(f"{average_compiled_duration}s")

    # time generic keybert
    keybert = KeyBERT(model=test_hf_pipeline)

    start = time.time()
    for i in range(n_runs):
        keybert.extract_keywords(test_documents)
    average_duration = (time.time() - start) / n_runs
    logger.info(f"Average generic keybert inference duration: {average_duration}s")

    assert average_duration >= (expected_speedup_factor * average_compiled_duration)
