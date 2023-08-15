# Standard Library
import shutil
from typing import List, Tuple

# 3rd party libraries
import numpy as np
import pytest

# Internal libraries
from onclusiveml.compile import CompiledPipeline


@pytest.mark.parametrize(
    "huggingface_pipeline_task, huggingface_model_reference",
    [
        (
            "feature-extraction",
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
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
        15,
        # None, # for 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', this is 512
        # and takes a long time for neuron tracing
    ],
)
def test_compiled_feature_extraction_pipeline_from_pretrained(
    huggingface_pipeline_task,
    huggingface_model_reference,
    huggingface_pipeline,
    max_length,
    batch_size,
    neuron,
    test_inputs,
    regression_test_atol,
    regression_test_rtol,
):
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
    compiled_pipeline_output: Tuple[Tuple[List[List[float]]]] = compiled_pipeline(
        test_inputs
    )  # 1 x n_batch x n_token x n_embed
    compiled_pipeline_output_arr: np.array = np.array(compiled_pipeline_output)
    # export and re-import compiled pipeline
    compiled_pipeline.save_pretrained("test_compiled_feature_extraction_pipeline")
    reloaded_compiled_pipeline = CompiledPipeline.from_pretrained(
        "test_compiled_feature_extraction_pipeline"
    )
    # score re-imported compiled pipeline
    reloaded_compiled_pipeline_output: Tuple[
        Tuple[List[List[float]]]
    ] = reloaded_compiled_pipeline(
        test_inputs
    )  # 1 x n_batch x n_token x n_embed
    reloaded_compiled_pipeline_output_arr: np.array = np.array(
        reloaded_compiled_pipeline_output
    )
    # validation: regression test embedding vectors
    np.testing.assert_allclose(
        reloaded_compiled_pipeline_output_arr,
        compiled_pipeline_output_arr,
        rtol=regression_test_rtol,
        atol=regression_test_atol,
    )

    shutil.rmtree("test_compiled_feature_extraction_pipeline")
