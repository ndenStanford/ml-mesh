# ML libs
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile import CompiledPipeline


@pytest.fixture(scope="session")
def test_hf_pipeline():

    return pipeline(
        task="token-classification",
        model="dslim/bert-base-NER",
    )


@pytest.fixture(scope="session")
def test_compiled_ner_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        pipeline=test_hf_pipeline,
        max_length=128,
        batch_size=6,
        neuron=False,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_ner_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        pipeline=test_hf_pipeline,
        max_length=128,
        batch_size=6,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture
def test_documents():

    return """Elon Reeve Musk (born June 28, 1971) is a business magnate and investor.
    He is the founder, CEO, and chief engineer of SpaceX; angel investor, CEO and product architect of Tesla, Inc.; owner and CTO of Twitter; founder of the Boring Company; co-founder of Neuralink and OpenAI; and president of the philanthropic Musk Foundation.
    Musk is the wealthiest person in the world with an estimated net worth, as of July 12, 2023, of around US$239 billion according to the Bloomberg Billionaires Index and $248.
    8 billion according to Forbes's Real Time Billionaires list, primarily from his ownership stakes in Tesla and SpaceX."""


