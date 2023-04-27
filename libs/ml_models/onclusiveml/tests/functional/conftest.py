# ML libs
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.ml_compile import CompiledPipeline


@pytest.fixture(scope="session")
def test_hf_pipeline():

    return pipeline(
        task="feature-extraction",
        model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    )


@pytest.fixture(scope="session")
def test_compiled_word_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=15,
        batch_size=1,
        neuron=False,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_compiled_document_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=150,  # test docs are <=120 words
        batch_size=1,
        neuron=False,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_word_pipeline(test_hf_pipeline):

    neuron_compiled_word_pipeline = CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=15,
        batch_size=1,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )

    neuron_compiled_word_pipeline.save_pretrained("neuron_compiled_word_pipeline")

    return neuron_compiled_word_pipeline


@pytest.fixture(scope="session")
def test_neuron_compiled_document_pipeline(test_hf_pipeline):

    neuron_compiled_document_pipeline = CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=150,  # test docs are <=120 words
        batch_size=1,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )

    neuron_compiled_document_pipeline.save_pretrained(
        "neuron_compiled_document_pipeline"
    )

    return neuron_compiled_document_pipeline


@pytest.fixture
def test_documents():

    return [
        # ~ 117 tokens
        """Machine learning is a subfield of artificial intelligence that involves training
        algorithms to make predictions or decisions based on data. It is a powerful tool for
        solving complex problems and has numerous applications in fields such as finance,
        healthcare, and transportation. In machine learning, the algorithm learns patterns and
        relationships from the data, rather than being explicitly programmed. This allows it to
        adapt and improve over time as more data becomes available. Machine learning models can be
        supervised, unsupervised, or semi-supervised.""",
        # ~ 115 tokens
        """ML Ops, also known as Machine Learning Operations, is a practice that focuses on the
        management and deployment of machine learning models in production environments. It
        combines the principles of DevOps, data engineering, and machine learning to ensure that ML
        models are deployed efficiently and reliably. ML Ops involves automating the entire machine
        learning lifecycle, from data preparation and model training to deployment and monitoring.
        This helps to enable faster iteration and experimentation.""",
        # ~ 110 tokens
        """Flowers come in different shapes, sizes, and colors, and their beauty has captivated
        humans for centuries. Apart from their aesthetic appeal, flowers are also essential to the
        ecosystem, playing a vital role in pollination necessary for the growth of crops and
        maintaining genetic diversity of plant species. Flowers have therapeutic properties and are
        used in traditional medicine for centuries. Chamomile, lavender, and marigold have soothing
        effects on the mind and body. The fragrance of flowers is calming, and they are used in
        aromatherapy worldwide. Flowers have cultural and emotional significance, often used in
        religious ceremonies, weddings, and funerals. Different flowers have symbolic meanings,
        such as lilies representing purity and innocence. Flowers are also a significant part of
        home decor, adding charm and personality to homes and gardens. In conclusion, flowers have
        multiple dimensions of significance.""",
    ]


@pytest.fixture
def test_document(test_documents, document_index: int = 0):

    return test_documents[document_index]
