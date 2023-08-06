"""Conftest"""

# ML libs
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile import CompiledPipeline


@pytest.fixture(scope="session")
def test_hf_pipeline():

    return pipeline(
        task="sentiment-analysis",
        model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
    )


@pytest.fixture(scope="session")
def test_compiled_sent_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        pipeline=test_hf_pipeline,
        max_length=128,
        batch_size=6,
        neuron=False,
        validate_compilation=False,
        # tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_sent_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        pipeline=test_hf_pipeline,
        max_length=128,
        batch_size=6,
        neuron=True,
        validate_compilation=False,
        # tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture
def test_documents():

    return (
        """Onclusive is a great company. London is a fantastic place."""  # noqa: E501
    )
