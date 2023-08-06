"""Functional Tests"""

# Standard Library
import time

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.sent import CompiledSent


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)


@pytest.mark.latency
@pytest.mark.parametrize(
    "compiled_sent_pipeline, n_runs, expected_speedup_factor",
    [
        (
            lazy_fixture("test_neuron_compiled_sent_pipeline"),
            50,
            1.1,
        ),
    ],
)
def test_compiled_sent_extract_sentiment_latency(
    compiled_sent_pipeline,
    test_hf_pipeline,
    test_document,
    n_runs,
    expected_speedup_factor,
):

    # time compiled sent
    compiled_sent = CompiledSent(
        compiled_sent_pipeline=compiled_sent_pipeline,
    )

    compiled_start = time.time()
    for i in range(n_runs):
        compiled_sent.extract_sentiment(test_document, return_pos=True)
    average_compiled_duration = (time.time() - compiled_start) / n_runs
    logger.info(
        f"Average compiled sent inference duration: {average_compiled_duration}s"
    )

    # time generic sent
    start = time.time()
    for i in range(n_runs):
        test_hf_pipeline(test_document)
    average_duration = (time.time() - start) / n_runs
    logger.info(f"Average generic sent inference duration: {average_duration}s")

    assert average_duration >= (expected_speedup_factor * average_compiled_duration)
