"""Functional Tests."""

# Standard Library
import time

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.ner import CompiledNER


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)


@pytest.mark.latency
@pytest.mark.parametrize(
    "compiled_ner_pipeline, n_runs, expected_speedup_factor",
    [
        (
            lazy_fixture("test_neuron_compiled_ner_pipeline"),
            50,
            1.1,
        ),
    ],
)
def test_compiled_ner_extract_entities_latency(
    compiled_ner_pipeline,
    test_hf_pipeline,
    test_document,
    n_runs,
    expected_speedup_factor,
):
    """
    Test latency performance of CompiledNER's extract_entities method. Measures inference duration
        of the CompiledNER class and compares it against inference time from a generic NER pipeline
    The purpose is to validate expected speedup factor achieved by the compiled model

    Args:
        compiled_ner_pipeline: Compiled NER pipeline fixture
        test_hf_pipeline: Test huggingface pipeline fixture
        test_document: Test document for NER inference
        n_runs: number of inference runs for averaging
        expected_speedup_factor: expected speedup factor for compiled ner model over generic
            ner model
    Returns:
        None
    Raises:
        AssertionError: If the average duration of generic ner model is not greater or requal
            to the expected speedup factor times the average duration of compiled model
    """

    # time compiled ner
    compiled_ner = CompiledNER(
        compiled_ner_pipeline=compiled_ner_pipeline,
    )

    compiled_start = time.time()
    for i in range(n_runs):
        compiled_ner.extract_entities(test_document, return_pos=True)
    average_compiled_duration = (time.time() - compiled_start) / n_runs
    logger.info(
        f"Average compiled ner inference duration: {average_compiled_duration}s"
    )

    # time generic ner
    start = time.time()
    for i in range(n_runs):
        test_hf_pipeline(test_document)
    average_duration = (time.time() - start) / n_runs
    logger.info(f"Average generic ner inference duration: {average_duration}s")

    assert average_duration >= (expected_speedup_factor * average_compiled_duration)
