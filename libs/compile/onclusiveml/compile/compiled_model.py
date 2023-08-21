# Standard Library
import json
import os
from pathlib import Path
from typing import Any, Dict, Tuple, Type, Union

# ML libs
import torch
import torch.neuron
from transformers import AutoConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.utils.generic import ModelOutput

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=20)


class CompiledModel(PreTrainedModel):
    """A fully functional subclass from the huggingface PreTrainedModel using a
    (neuron-)torchscript model as backend. Includes
    - the pseduo-constructor method `from_model`: Automatically (neuron-)traces
        a specified pytorch model or huggingface transformer model and returns a
        CompiledModel instance.
    - Adapted postprocessing for torch.nn.Modules returning dictionaries
    - canonical export and import methods `save_pretrained` & `from_pretrained`,
        supporting the persistence of key (neuron-)tracing configuration parameters."""

    @classmethod
    def from_model(
        cls,
        model: PreTrainedModel,
        batch_size: int = 1,
        max_length: int = -1,
        neuron: bool = True,
        validate_compilation: bool = True,
        validation_rtol: float = 1e-02,
        validation_atol: float = 1e-02,
        **tracing_kwargs: Any
    ) -> "CompiledModel":
        """Takes a huggingface transformer model, compiles it according to specified
        configuration and returns a fully instantiated CompiledModel instance together with
        the (neuron-)tracing configuration.

        model (PreTrainedModel): The huggingface pytorch model or pytorch nn.module to compile
        batch_size (int, optional): The size of the batch used for tracing
        max_length (_type_): The number of tokens per record used for tracing, e.g. input sequence
            length
        neuron (bool, optional): If True, uses torch.neuron.trace for compilation,
            otherwise uses torch.jit.trace. Defaults to True.
        validate_compilation (bool, optional): If True, runs a simple regression test comparing the
            specified model's outputs with the newly compiled model's outputs, using the tracing
            inputs as pseudo-tokens
        validation_rtol (float, optional): The relative deviation threshold. Only relevant when
            validate_compilation=True.
        validation_atol (float, optional): The absolute deviation threshold. Only relevant when
            validate_compilation=True.
        **tracing_kwargs:
            dynamic_batching (bool, optional): If True, traced model allows for
                variable batch sizes during inference up to the batch_size used during compilation.
                Defaults to True.
            strict (bool, optional): If True, enforces deterministic inference behaviour during
                tracing. In particular, requires the model arg to have return_dict=False.
            compiler_args (List[str], optional): Note: Not setting these was
                observed to lead to NaN during inference on huggingface==4.27.x & torch==1.12.1.
                Defaults to ['--fast-math','none'].
        """
        # ensure reasonable defaults and required specs for functional neuron tracing
        if max_length == -1:
            max_length = model.config.max_position_embeddings
        # for neuron tracing, the following parameters are either required or beneficial
        if neuron is True:
            # allows for dynamic batch size during inference
            tracing_kwargs["dynamic_batch_size"] = tracing_kwargs.get(
                "dynamic_batch_size", True
            )
            # ensures all ops are getting traced; required when enabling dynamic batching for some
            # models, as per https://github.com/aws-neuron/aws-neuron-sdk/issues/613
            tracing_kwargs["fallback"] = tracing_kwargs.get("fallback", False)
            # required to avoid NaN output at inference for some models
            tracing_kwargs["compiler_args"] = tracing_kwargs.get(
                "compiler_args", ["--fast-math", "none"]
            )
        # torch.nn.Module s returning dicts can still be traced - see `forward` method
        tracing_kwargs["strict"] = tracing_kwargs.get("strict", False)
        # trace model and return fuilly functional custom model class instance
        traced_model, tracing_inputs, compilation_specs = compile_model(
            model,
            batch_size=batch_size,
            max_length=max_length,
            neuron=neuron,
            **tracing_kwargs
        )
        # instatiate the model from config
        compiled_model = cls(model.config)
        # replace model attribute with traced model & attach compilation config dict
        compiled_model.model = traced_model
        compiled_model.compilation_specs = compilation_specs
        # if desired, run a quick regression test using the tracing inputs: original model vs newly
        # traced model
        if validate_compilation is True:
            tracing_inputs_dict = {
                "input_ids": tracing_inputs[0],
                "attention_mask": tracing_inputs[1],
            }

            model_output = model(**tracing_inputs_dict)
            # When return_dict = True
            if not isinstance(model_output, torch.Tensor):
                model_output = model_output[0]

            traced_model_output = compiled_model(**tracing_inputs_dict)

            torch.testing.assert_close(
                model_output,
                traced_model_output,
                atol=validation_atol,
                rtol=validation_rtol,
            )

        return compiled_model

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor = None,
        **kwargs: Any
    ) -> ModelOutput:
        self.return_dict = kwargs.pop("return_dict", None)

        # traced model requires positional arguments
        model_output = self.model(input_ids, attention_mask)
        if not self.return_dict:
            return model_output["logits"]

        # if original model graph returns a dict, convert to data type that can handle both
        # - integer and
        # - string-key based
        #  indexing
        if isinstance(model_output, dict):
            logger.debug("Model output is a dictionary. Converting")
            model_output = ModelOutput(model_output)

        return model_output

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """Canonic huggingface transformers export method. Only supports exporting to local file
        system.

        Args:
            directory (Path,str): Directory on local file system to export model artifact to. Will
                be created if it doesnt exist.
        """
        # export remaining huggingface PreTrainedModel context
        self.config.save_pretrained(directory)
        # export traced model in torchscript format
        torch.jit.save(self.model, os.path.join(directory, "model.pt"))
        # export compilation configuration dict
        with open(
            os.path.join(directory, "compilation_specs.json"), "w"
        ) as compilation_specs_file:
            json.dump(self.compilation_specs, compilation_specs_file)

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledModel":
        """Canonic huggingface transformers import method. Only supports importing from local file
        system.

        Args:
            directory (Path,str): Directory on local file system to import model artifact from."""
        # import and instantiate huggingface transformer config
        config = AutoConfig.from_pretrained(directory)
        # use huggingface transformer PreTrainedModel constructor to re-initialize the original
        # model's class' instance from config
        compiled_model = cls(config)
        # switch out model attribute with re-imported (neuron-)torchscript model
        compiled_model.model = torch.jit.load(os.path.join(directory, "model.pt"))
        # re-import and attach compilation configuration dict
        with open(
            os.path.join(directory, "compilation_specs.json"), "r"
        ) as compilation_specs_file:
            compiled_model.compilation_specs = json.load(compilation_specs_file)

        return compiled_model


def compile_model(
    model: Type[PreTrainedModel],
    batch_size: int,
    max_length: int,
    neuron: bool = True,
    **tracing_kwargs: Any
) -> Tuple[
    torch.jit._trace.TopLevelTracedModule,
    Tuple[torch.Tensor, torch.Tensor],
    Dict[str, Any],
]:
    """Utility function for (neuron-)tracing a torch hugginface model to either torchscript or
    neuron torchscript.

    Returns the traced model object, the inputs used for tracing and the tracing configuration.

    Args:
        model (_type_): The huggingface pytorch model or pytorch nn.module to compile
        batch_size (_type_): The size of the batch used for tracing
        max_length (_type_): The number of tokens per record used for tracing, e.g. input sequence
            length
        neuron (bool, optional): _description_. If True, uses torch.neuron.trace for compilation,
            otherwise uses torch.jit.trace. Defaults to True.
        **tracing_kwargs: Keyword arguments passed onto
            - the `torch.neuron.trace` method if `neuron`=True
            - the `torch.jit.trace` method if `neuron`=False
    """
    # generate tracing inputs according to specs
    tracing_inputs = (
        torch.zeros((batch_size, max_length), dtype=torch.long),  # input_ids
        torch.zeros((batch_size, max_length), dtype=torch.long),  # attention_mask
    )

    if neuron:
        traced_model = torch.neuron.trace(model, tracing_inputs, **tracing_kwargs)
    else:
        traced_model = torch.jit.trace(model, tracing_inputs, **tracing_kwargs)

    compilation_specs = dict(
        **{"tracing_kwargs": tracing_kwargs},
        **{
            "tracing__batch_size": batch_size,
            "tracing__max_length": max_length,
            "tracing__neuron": neuron,
        }
    )

    return traced_model, tracing_inputs, compilation_specs
