# 1 Overview

The `compile` library provides a tested framework to consistently compile and export/import
[`transformers` library](https://github.com/huggingface/transformers) based, torch-flavoured  models.

In particular, it leverages [the AWS Neuron accelerator](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/)
 to provide a consistent API for compiling

- tokenizer
- model
- pipeline

objects to neuron-torch, and persisting them after compilation.

Note: [A new, official AWS <-> huggingface integration library has sprung up recently](https://github.com/huggingface/optimum-neuron)
 that has significant overlap with this internally maintained one. It is suggested to monitor and
  migrate to it when the necessary levels of functionality and stability has been reached.

# 2 Content

There are three main modules, each implementing a `Compiled...` version of the following core
huggingface classes, respectively:

- `compiled_tokenizer.py`: Implements the `CompiledTokenizer` class
- `compiled_model.py`: Implements the `CompiledModel` class
- `compiled_pipeline.py`: Implements the `CompiledPipeline` class.

All of these classes have been specifically designed to retain their canonical `huggingface`
"behaviour", i.e. you can interact with them in very much the same way you would with their
uncompiled versions. This includes:

- the use `from_pretrained` and `save_pretrained` for initialization and persisting to disk,
  respectively
- the use the __call__ methods to run inference
- access to all relevant uncompiled class' version's attributes and methods at the `Compiled...`
  version's class level
  - e.g. the `CompiledTokenizer` will make the `._tokenizer` attribute of the uncompiled tokenizer
    available at the same `_tokenizer` attribute handle
  - e.g. the `CompiledPipeline` will make the `model` attribute of the uncompiled pipeline available
    at the same `model` attribute handle
  - etc.

# 3 Usage

For details on how to use the `CompiledTokenizer`, `CompiledModel` and `CompiledPipeline` classes,
see the respective `functional` test suite(s).

# 4 Tests

Before you run any tests, make sure you have installed the `compile` library on your development
instance using an up-to-date poetry lock file.

## Unit

To run the unit test suite, simply run

```make libs.unit/compile```

## Integration

N/A

## Functional

To run the functional test suite, simply run

```make libs.functional/compile```.
