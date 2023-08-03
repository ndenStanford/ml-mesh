# ML libs
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    Trainer,
    TrainingArguments,
)
from transformers.trainer_pt_utils import get_parameter_names

# 3rd party libraries
import bitsandbytes as bnb
from accelerate import Accelerator
from pynvml import nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlInit


def print_gpu_utilization():
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    print(f"GPU memory occupied: {info.used//1024**2} MB.")


def print_summary(result):
    print(f"Time: {result.metrics['train_runtime']:.2f}")
    print(f"Samples/second: {result.metrics['train_samples_per_second']:.2f}")
    print_gpu_utilization()


DEFAULT_ARGS = {
    "output_dir": "tmp",
    "evaluation_strategy": "steps",
    "num_train_epochs": 1,
    "optim": "adafactor",
    "log_level": "error",
    "report_to": "none",
}


def test_training_gpu(test_train_dataset, test_model_reference):
    """Checks transformers library ability to use GPU device for vanilla training
    (without accelerate)"""

    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )

    training_args = TrainingArguments(
        per_device_train_batch_size=4, fp16=True, **DEFAULT_ARGS
    )
    trainer = Trainer(model=model, args=training_args, train_dataset=test_train_dataset)
    result = trainer.train()

    print_summary(result)


def test_training_w_optimizer_gpu(test_train_dataset, test_model_reference):
    """Checks transoformers library abilitiy to use GPU device for 8bit optimizer-based training
    (without accelerate)"""
    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )
    training_args = TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        fp16=True,
        **DEFAULT_ARGS,
    )
    # create bnb optimizer
    decay_parameters = get_parameter_names(model, [torch.nn.LayerNorm])
    decay_parameters = [name for name in decay_parameters if "bias" not in name]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if n in decay_parameters],
            "weight_decay": training_args.weight_decay,
        },
        {
            "params": [
                p for n, p in model.named_parameters() if n not in decay_parameters
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer_kwargs = {
        "betas": (training_args.adam_beta1, training_args.adam_beta2),
        "eps": training_args.adam_epsilon,
    }
    optimizer_kwargs["lr"] = training_args.learning_rate
    adam_bnb_optim = bnb.optim.Adam8bit(
        optimizer_grouped_parameters,
        betas=(training_args.adam_beta1, training_args.adam_beta2),
        eps=training_args.adam_epsilon,
        lr=training_args.learning_rate,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=test_train_dataset,
        optimizers=(adam_bnb_optim, None),
    )
    result = trainer.train()
    print_summary(result)


def test_accelerated_training_w_optimizer_gpu(test_train_dataset, test_model_reference):
    """Checks transoformers library abilitiy to use GPU device for 8bit optimizer-based training
    using the accelerate extension library"""
    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )
    training_args = TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        gradient_checkpointing=True,
        **DEFAULT_ARGS,
    )
    # create bnb optimizer
    decay_parameters = get_parameter_names(model, [torch.nn.LayerNorm])
    decay_parameters = [name for name in decay_parameters if "bias" not in name]
    optimizer_grouped_parameters = [
        {
            "params": [p for n, p in model.named_parameters() if n in decay_parameters],
            "weight_decay": training_args.weight_decay,
        },
        {
            "params": [
                p for n, p in model.named_parameters() if n not in decay_parameters
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer_kwargs = {
        "betas": (training_args.adam_beta1, training_args.adam_beta2),
        "eps": training_args.adam_epsilon,
    }
    optimizer_kwargs["lr"] = training_args.learning_rate
    adam_bnb_optim = bnb.optim.Adam8bit(
        optimizer_grouped_parameters,
        betas=(training_args.adam_beta1, training_args.adam_beta2),
        eps=training_args.adam_epsilon,
        lr=training_args.learning_rate,
    )
    dataloader = torch.utils.data.dataloader.DataLoader(
        test_train_dataset, batch_size=training_args.per_device_train_batch_size
    )
    if training_args.gradient_checkpointing:
        model.gradient_checkpointing_enable()
    accelerator = Accelerator(mixed_precision="fp16")
    model, optimizer, dataloader = accelerator.prepare(
        model, adam_bnb_optim, dataloader
    )
    model.train()
    for step, batch in enumerate(dataloader, start=1):
        loss = model(**batch).loss
        loss = loss / training_args.gradient_accumulation_steps
        accelerator.backward(loss)
        if step % training_args.gradient_accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()


def test_bert_inference_gpu(test_model_reference):
    """Checks transformers library ability to use GPU device for tokenizing * inference"""

    tokenizer = AutoTokenizer.from_pretrained(test_model_reference)
    model = AutoModelForSequenceClassification.from_pretrained(test_model_reference).to(
        "cuda"
    )

    inputs = tokenizer("Hello World!", return_tensors="pt").to("cuda")
    model(**inputs)
