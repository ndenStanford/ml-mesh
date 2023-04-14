# Standard Library
from typing import List, Tuple

# 3rd party libraries
import numpy as np
import pandas as pd
import pytest

# Internal libraries
from onclusiveml.ml_compile import CompiledPipeline


@pytest.mark.parametrize(
    "huggingface_pipeline_task, huggingface_model_reference",
    [("text-classification", "prajjwal1/bert-tiny")],
)
@pytest.mark.parametrize("neuron", [True, False])  # regular torchscript
@pytest.mark.parametrize("batch_size", [1, 4, 8])
@pytest.mark.parametrize(
    "max_length",
    [
        15,
        # None, # for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', this is 512
        # and takes a long time for neuron tracing
    ],
)
def test_compiled_text_classification_pipeline_from_pipeline(
    huggingface_pipeline_task,
    huggingface_model_reference,
    huggingface_pipeline,
    max_length,
    batch_size,
    neuron,
    sample_inputs,
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
    compiled_pipeline_output: Tuple[Tuple[List[List[float]]]] = compiled_pipeline(
        sample_inputs
    )  # 1 x n_batch x n_token x n_embed
    compiled_pipeline_output_df = pd.DataFrame(compiled_pipeline_output)
    # score huggingface pipeline
    huggingface_pipeline_output: Tuple[Tuple[List[List[float]]]] = huggingface_pipeline(
        sample_inputs,
        truncation=True,
        add_special_tokens=True,
        padding="max_length",
        max_length=max_length,
    )
    huggingface_pipeline_output_df = pd.DataFrame(huggingface_pipeline_output)
    # validation: regression test labels and logits
    pd.testing.assert_series_equal(
        huggingface_pipeline_output_df["label"], compiled_pipeline_output_df["label"]
    )
    np.testing.assert_allclose(
        huggingface_pipeline_output_df["score"].values,
        compiled_pipeline_output_df["score"].values,
        rtol=regression_test_rtol,
        atol=regression_test_atol,
    )
