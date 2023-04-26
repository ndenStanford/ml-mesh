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
        max_length=150,  # test docs are 100 words, so should be <= 150 tokens
        batch_size=1,
        neuron=False,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_word_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=10,
        batch_size=1,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_document_pipeline(test_hf_pipeline):

    return CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=15,
        batch_size=1,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture
def test_documents():

    return [
        """Machine learning is a subfield of artificial intelligence that involves training
        algorithms to make predictions or decisions based on data. It is a powerful tool for
        solving complex problems and has numerous applications in fields such as finance,
        healthcare, and transportation. In machine learning, the algorithm learns patterns and
        relationships from the data, rather than being explicitly programmed. This allows it to
        adapt and improve over time as more data becomes available. Machine learning models can be
        supervised, unsupervised, or semi-supervised, depending on the type of data and the problem
        being solved. As more data is generated and computing power increases, the possibilities
        for machine learning are only growing.""",
        """ML Ops, also known as Machine Learning Operations, is a practice that focuses on the
        management and deployment of machine learning models in production environments. It
        combines the principles of DevOps, data engineering, and machine learning to ensure that ML
        models are deployed efficiently and reliably. ML Ops involves automating the entire machine
        learning lifecycle, from data preparation and model training to deployment and monitoring.
        This helps to improve the scalability and performance of ML models, reduce downtime, and
        enable faster iteration and experimentation. As the demand for AI and ML continues to grow,
        ML Ops is becoming an essential practice for organizations that want to achieve success
        with their machine learning initiatives.""",
        """ChatGPT is a large language model trained by OpenAI, based on the GPT-3.5 architecture.
        It is designed to engage in natural language conversations with humans and assist them in
        various tasks. ChatGPT is capable of understanding and generating human-like responses,
        which makes it a useful tool for a wide range of applications, including customer service,
        language translation, and content creation. It uses machine learning algorithms to learn
        from its interactions with users and continuously improve its performance. ChatGPT has been
        trained on a massive corpus of text data, including books, articles, and websites, which
        gives it a broad knowledge base to draw upon. Overall, ChatGPT represents a significant
        advancement in natural language processing and has the potential to revolutionize the way
        humans interact with machines.""",
    ]
