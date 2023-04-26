# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.ml_models.keywords import CustomHFTransformerBackend


@pytest.mark.order(1)
@pytest.mark.backend
@pytest.mark.parametrize("invalid_pipeline_type", ["some string value"])
def custom_hf_transformer_backend___init__raise_test(invalid_pipeline_type):

    with pytest.raises(ValueError):
        CustomHFTransformerBackend(embedding_model=invalid_pipeline_type)


@pytest.mark.order(1)
@pytest.mark.backend
@pytest.mark.parametrize(
    "compiled_pipeline",
    [
        lazy_fixture("test_hf_pipeline"),
        lazy_fixture("test_compiled_word_pipeline"),
        lazy_fixture("test_neuron_compiled_word_pipeline"),
    ],
)
def custom_hf_transformer_backend_embed_test(compiled_pipeline, test_documents):

    compiled_hf_backend = CustomHFTransformerBackend(embedding_model=compiled_pipeline)

    test_embeddings = compiled_hf_backend.embed(test_documents)

    assert len(test_embeddings) == len(test_documents)
