# Standard Library
import os

# ML libs
import torch
import torch.neuron
from transformers import AutoModel, AutoModelForSequenceClassification
from transformers.pipelines import pipeline

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile import CompiledModel, CompiledPipeline


@pytest.mark.core
@pytest.mark.compilation
@pytest.mark.parametrize(
    "huggingface_model_reference,huggingface_model_type,export_handle",
    [
        (
            "prajjwal1/bert-tiny",
            AutoModelForSequenceClassification,
            "text-classification-model",
        ),
        ("prajjwal1/bert-tiny", AutoModel, "feature-extraction-model"),
    ],
)
def create_and_save_neuron_compiled_model_test(
    huggingface_model_reference, huggingface_model_type, test_output_dir, export_handle
) -> None:

    huggingface_model = huggingface_model_type.from_pretrained(
        huggingface_model_reference
    )
    huggingface_model.eval()

    neuron_compiled_model = CompiledModel.from_model(
        model=huggingface_model,
        max_length=5,
        batch_size=2,
        neuron=True,
        validate_compilation=False,  # this would require the ability to score a neuron model
    )

    neuron_compiled_model.save_pretrained(os.path.join(test_output_dir, export_handle))


@pytest.mark.inference
@pytest.mark.parametrize(
    "export_handle",
    [
        ("text-classification-model"),  # task: text-classification
        ("feature-extraction-model"),  # task: feature-extraction
    ],
)
def load_and_score_neuron_compiled_model_test(export_handle, test_output_dir):

    neuron_compiled_model = CompiledModel.from_pretrained(
        os.path.join(test_output_dir, export_handle)
    )
    # demonstrate retrieving neuron model meta data
    # note that retrieving batch size is not required as dynamic batching was enabled
    # by default during compilation
    model_batch_size = neuron_compiled_model.compilation_specs["tracing__batch_size"]
    model_max_length = neuron_compiled_model.compilation_specs["tracing__max_length"]
    # force the dynamic batching chunking by adding one row to the batch size
    model_inputs = {
        "input_ids": torch.ones(
            (model_batch_size + 1, model_max_length), dtype=torch.long
        ),
        "attention_mask": torch.ones(
            (model_batch_size + 1, model_max_length), dtype=torch.long
        ),
    }

    neuron_compiled_model(**model_inputs)


@pytest.mark.core
@pytest.mark.compilation
@pytest.mark.parametrize(
    "huggingface_model_reference,huggingface_pipeline_task",
    [
        ("prajjwal1/bert-tiny", "text-classification"),
        ("prajjwal1/bert-tiny", "feature-extraction"),
    ],
)
def create_and_save_neuron_compiled_pipeline_test(
    huggingface_model_reference, huggingface_pipeline_task, test_output_dir
):

    huggingface_pipeline = pipeline(
        task=huggingface_pipeline_task, model=huggingface_model_reference
    )

    neuron_compiled_pipeline = CompiledPipeline.from_pipeline(
        pipeline=huggingface_pipeline,
        max_length=5,
        batch_size=2,
        neuron=True,
        validate_compilation=False,
    )

    neuron_compiled_pipeline.save_pretrained(
        os.path.join(test_output_dir, huggingface_pipeline_task)
    )


@pytest.mark.inference
@pytest.mark.parametrize(
    "huggingface_pipeline_task", [("text-classification"), ("feature-extraction")]
)
def load_and_score_neuron_compiled_pipeline_test(
    huggingface_pipeline_task, test_output_dir, torch_model_text_input
):

    neuron_compiled_pipeline = CompiledPipeline.from_pretrained(
        os.path.join(test_output_dir, huggingface_pipeline_task)
    )

    neuron_compiled_pipeline(torch_model_text_input)
