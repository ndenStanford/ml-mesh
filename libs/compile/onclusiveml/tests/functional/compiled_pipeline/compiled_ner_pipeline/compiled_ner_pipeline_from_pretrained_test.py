"""Compiled NER pipeline from pretrained test."""

# Standard Library
import shutil
from typing import Dict, List

# 3rd party libraries
import pandas as pd
import pytest

# Internal libraries
from onclusiveml.compile import CompiledPipeline


@pytest.mark.parametrize(
    "huggingface_pipeline_task, huggingface_model_reference",
    [
        (
            "ner",
            "dslim/bert-base-NER",
        ),
    ],
)
@pytest.mark.parametrize("neuron", [True, False])  # regular torchscript
@pytest.mark.parametrize(
    "batch_size",
    [
        4,
    ],
)
@pytest.mark.parametrize(
    "max_length",
    [
        35,
        # None, # for 'dslim/bert-base-NER', this is 512
        # and takes a long time for neuron tracing
    ],
)
def test_compiled_token_classification_pipeline_from_pretrained(
    huggingface_pipeline_task,
    huggingface_model_reference,
    huggingface_pipeline,
    max_length,
    batch_size,
    neuron,
    test_ner_inputs,
    regression_test_atol,
    regression_test_rtol,
):
    """Test compiled token classification pipeline from pretrained."""
    # create new pipeline using compiled versions of tokenizer and model
    compiled_pipeline = CompiledPipeline.from_pipeline(
        huggingface_pipeline,
        max_length=max_length,
        batch_size=batch_size,
        neuron=neuron,
        validate_compilation=True,
        validation_rtol=regression_test_rtol,
        validation_atol=regression_test_atol,
        tokenizer_settings={"add_special_tokens": True},
    )
    # score compiled pipeline
    compiled_pipeline_output: List[Dict] = compiled_pipeline(test_ner_inputs)

    compiled_pipeline_output_df = pd.concat(
        [pd.DataFrame(named_entity) for named_entity in compiled_pipeline_output]
    )
    # export and re-import compiled pipeline
    compiled_pipeline.save_pretrained("test_compiled_ner_pipeline")
    reloaded_compiled_pipeline = CompiledPipeline.from_pretrained(
        "test_compiled_ner_pipeline"
    )
    # score huggingface pipeline
    reloaded_compiled_pipeline_output: List[Dict] = reloaded_compiled_pipeline(
        test_ner_inputs
    )

    reloaded_compiled_pipeline_output_df = pd.concat(
        [
            pd.DataFrame(named_entity)
            for named_entity in reloaded_compiled_pipeline_output
        ]
    )
    # validation: regression test extracted named entity scores and other meta data
    pd.testing.assert_frame_equal(
        compiled_pipeline_output_df,
        reloaded_compiled_pipeline_output_df,
        rtol=regression_test_rtol,
        atol=regression_test_atol,
    )

    shutil.rmtree("test_compiled_ner_pipeline")
