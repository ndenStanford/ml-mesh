"""Integration Tests"""

# Standard Library
import shutil

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.sentiment import CompiledSent


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)


@pytest.mark.parametrize(
    "compiled_sent_pipeline",
    [
        lazy_fixture("test_compiled_sent_pipeline"),
        lazy_fixture("test_neuron_compiled_sent_pipeline"),
    ],
)
def test_compiled_sent_extract_sent(compiled_sent_pipeline, test_documents):

    compiled_sent = CompiledSent(compiled_sent_pipeline=compiled_sent_pipeline)

    test_compiled_sent = compiled_sent.extract_sentiment(test_documents)
    assert len(test_compiled_sent) > 0


@pytest.mark.parametrize(
    "compiled_sent_pipeline",
    [
        lazy_fixture("test_compiled_sent_pipeline"),
        lazy_fixture("test_neuron_compiled_sent_pipeline"),
    ],
)
def test_compiled_sent_save_pretrained_from_pretrained(
    compiled_sent_pipeline, test_documents
):
    # initialize with constructor and score
    compiled_sent = CompiledSent(
        compiled_sent_pipeline=compiled_sent_pipeline,
    )

    test_compiled_sentiment = compiled_sent.extract_sentiment(test_documents)

    # save, load and score again
    compiled_sent.save_pretrained("./test")
    compiled_sent_reloaded = CompiledSent.from_pretrained("./test")

    test_compiled_sentiment_reloaded = compiled_sent_reloaded.extract_sentiment(
        test_documents
    )

    assert test_compiled_sentiment == test_compiled_sentiment_reloaded
    # clean up
    shutil.rmtree("./test")
