"""Transformers GPU tests."""

# ML libs
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)

# 3rd party libraries
import pytest
from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


def gpu_utilization():
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    memory_used_mb = info.used // 1024**2

    return memory_used_mb


def print_train_summary(result):
    print(f"Time: {result.metrics['train_runtime']:.2f}")
    print(f"Samples/second: {result.metrics['train_samples_per_second']:.2f}")


@pytest.mark.order(6)
def test_training_gpu(
    test_train_dataset, test_model_reference, test_default_training_params
):
    """Checks transformers library ability to use GPU device for training"""

    print(f"GPU device reserved memory (before training): {gpu_utilization()}")

    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )

    training_args = TrainingArguments(
        per_device_train_batch_size=4, fp16=True, **test_default_training_params
    )
    trainer = Trainer(model=model, args=training_args, train_dataset=test_train_dataset)
    result = trainer.train()

    print_train_summary(result)
    # GPU memory used should be more than 2GB
    gpu_memory = gpu_utilization()
    print(f"GPU device reserved memory (after training): {gpu_memory}")
    assert gpu_memory > 2000


@pytest.mark.order(7)
def test_inference_gpu(test_model_reference):
    """Checks transformers library ability to use GPU device for tokenizing & inference"""

    print(f"GPU device reserved memory (before inference): {gpu_utilization()}")

    tokenizer = AutoTokenizer.from_pretrained(test_model_reference)
    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )

    inputs = tokenizer("Hello World!", return_tensors="pt").to("cuda")

    print(
        f"GPU device reserved memory (after model load, before inference): {gpu_utilization()}"
    )

    model(**inputs)

    print(f"GPU device reserved memory (after inference): {gpu_utilization()}")
