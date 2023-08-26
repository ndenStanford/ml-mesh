"""Custom HF transformer backend tests."""

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.models.keywords import CustomHFTransformerBackend


@pytest.mark.order(1)
@pytest.mark.backend
@pytest.mark.parametrize("invalid_pipeline_type", ["some string value"])
def test_custom_hf_transformer_backend___init__raise(invalid_pipeline_type):

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
def test_custom_hf_transformer_backend_embed(compiled_pipeline, test_documents):

    compiled_hf_backend = CustomHFTransformerBackend(embedding_model=compiled_pipeline)

    test_embeddings = compiled_hf_backend.embed(test_documents)

    assert len(test_embeddings) == len(test_documents)
