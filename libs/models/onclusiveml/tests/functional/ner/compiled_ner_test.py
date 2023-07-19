# Standard Library
import time

# 3rd party libraries
import pandas as pd
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

    # time compiled ner
    compiled_ner = CompiledNER(
        compiled_ner_pipeline=compiled_ner_pipeline,
    )

    compiled_start = time.time()
    for i in range(n_runs):
        compiled_ner.extract_entities(test_document, return_pos=True)
    average_compiled_duration = (time.time() - compiled_start) / n_runs
    logger.info(f"Average compiled ner inference duration: ")
    logger.info(f"{average_compiled_duration}s")

    # time generic ner
    start = time.time()
    for i in range(n_runs):
        test_hf_pipeline(test_document)
    average_duration = (time.time() - start) / n_runs
    logger.info(f"Average generic ner inference duration: {average_duration}s")

    assert average_duration >= (expected_speedup_factor * average_compiled_duration)
