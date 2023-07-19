# Standard Library
import shutil

# 3rd party libraries
import pytest
from pytest_lazyfixture import lazy_fixture

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.ner import CompiledNER


logger = get_default_logger(__name__, level=20, fmt=LogFormat.DETAILED.value)

@pytest.mark.parametrize(
    "compiled_ner_pipeline",
    [
        lazy_fixture("test_compiled_ner_pipeline"),
        lazy_fixture("test_neuron_compiled_ner_pipeline"),
    ],
)
def test_compiled_ner_extract_ner(
    compiled_ner_pipeline, test_documents
):

    compiled_ner = CompiledNER(compiled_ner_pipeline=compiled_ner_pipeline)

    test_compiled_ner = compiled_ner.extract_entities(sentences=test_documents, return_pos=True)
    assert len(test_compiled_ner)>0



@pytest.mark.parametrize(
    "compiled_ner_pipeline",
    [
        lazy_fixture("test_compiled_ner_pipeline"),
        lazy_fixture("test_neuron_compiled_ner_pipeline"),
    ],
)
def test_compiled_ner_save_pretrained_from_pretrained(
    compiled_ner_pipeline, test_documents
):
    # initialize with constructor and score
    compiled_ner = CompiledNER(
        compiled_ner_pipeline=compiled_ner_pipeline,
    )

    test_compiled_entities = compiled_ner.extract_entities(sentences=test_documents, return_pos=True)

    # save, load and score again
    compiled_ner.save_pretrained("./test")
    compiled_ner_reloaded = CompiledNER.from_pretrained("./test")

    test_compiled_entities_reloaded = compiled_ner_reloaded.extract_entities(
        sentences=test_documents, return_pos=True
    )

    assert test_compiled_entities == test_compiled_entities_reloaded
    # clean up
    shutil.rmtree("./test")
