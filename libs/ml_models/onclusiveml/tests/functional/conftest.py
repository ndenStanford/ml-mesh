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
        max_length=512,  # test docs are 100 words, so should be <= 300 tokens
        batch_size=1,
        neuron=False,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )


@pytest.fixture(scope="session")
def test_neuron_compiled_word_pipeline(test_hf_pipeline):

    # try:
    #     neuron_compiled_word_pipeline = CompiledPipeline.from_pretrained(
    #         "neuron_compiled_word_pipeline"
    #     )
    # except:
    neuron_compiled_word_pipeline = CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=25,
        batch_size=3,
        neuron=True,
        validate_compilation=False,
        tokenizer_settings={"add_special_tokens": True},
    )

    neuron_compiled_word_pipeline.save_pretrained("neuron_compiled_word_pipeline")

    return neuron_compiled_word_pipeline


@pytest.fixture(scope="session")
def test_neuron_compiled_document_pipeline(test_hf_pipeline):

    # try:
    #     neuron_compiled_document_pipeline = CompiledPipeline.from_pretrained(
    #         "neuron_compiled_document_pipeline"
    #     )
    # except:
    neuron_compiled_document_pipeline = CompiledPipeline.from_pipeline(
        test_hf_pipeline,
        max_length=512,
        batch_size=3,
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
        multiple dimensions of significance."""
        # ~ 500 tokens
        """Flowers are nature's way of displaying beauty and elegance. They come in various colors,
        shapes, and sizes, and their attractiveness has fascinated humans for centuries. However,
        flowers have more to offer than their aesthetic value, and they play a crucial role in the
        ecosystem. Flowers are the reproductive organs of plants, and they play a vital role in
        pollination. They produce nectar and pollen that attract pollinators such as bees,
        butterflies, and hummingbirds, who transfer pollen from the stamen to the stigma of the
        flowers. This process helps in the fertilization of plants and is essential for the growth
        of crops and other vegetation. Flowers also ensure the genetic diversity of plant species.
        Apart from their ecological significance, flowers have numerous medicinal benefits. Many
        flowers have therapeutic properties that have been used in traditional medicine for
        centuries. For instance, chamomile is known for its calming effects and is used to treat
        anxiety and insomnia. Lavender is also used to promote relaxation, relieve pain, and
        improve sleep quality. Flowers like calendula have anti-inflammatory and antiseptic
        properties and can be used to treat skin infections and wounds. Moreover, flowers have an
        essential aesthetic value. They add color, charm, and personality to homes and gardens.
        The beauty of flowers is mesmerizing and captivating, and it has a calming effect on the
        mind and soul. Flowers arrangements, whether simple or elaborate, have a significant impact
        on the overall aesthetic appeal of a space. In conclusion, flowers are not just pretty
        things to look at. They have significant ecological, medicinal, cultural, and aesthetic
        values. They play a vital role in the ecosystem, ensuring the growth of crops and
        maintaining genetic diversity of plant species. Flowers also have therapeutic properties
        and are used in traditional medicine worldwide. They are an essential part of cultural
        traditions and are used to express emotions. The beauty and charm of flowers are
        mesmerizing and captivating, and it adds personality and charm to homes and gardens.
        Flowers are more than just plants; they are essential to human life and bring happiness and
        joy to those who admire them..""",
    ]


@pytest.fixture
def test_document(test_documents, document_index: int = 0):

    return test_documents[document_index]
