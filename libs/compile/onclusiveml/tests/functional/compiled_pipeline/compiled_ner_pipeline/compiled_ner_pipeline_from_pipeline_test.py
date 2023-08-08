# Standard Library
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
@pytest.mark.parametrize("batch_size", [1, 2, 4])
@pytest.mark.parametrize(
    "max_length",
    [
        35,
        # None, # for 'dslim/bert-base-NER', this is 512
        # and takes a long time for neuron tracing
    ],
)
def test_compiled_token_classification_pipeline_from_pipeline(
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
    # create compiled pipeline
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
    # score huggingface pipeline
    huggingface_pipeline_output: List[Dict] = huggingface_pipeline(test_ner_inputs)

    huggingface_pipeline_output_df = pd.concat(
        [pd.DataFrame(named_entity) for named_entity in huggingface_pipeline_output]
    )
    # validation: regression test extracted named entity scores and other meta data
    pd.testing.assert_frame_equal(
        compiled_pipeline_output_df,
        huggingface_pipeline_output_df,
        rtol=regression_test_rtol,
        atol=regression_test_atol,
    )
