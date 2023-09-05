"""Compiled tokenizer."""

# Standard Library
import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Union

# ML libs
from transformers import (
    AutoTokenizer,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

# Internal libraries
from onclusiveml.compile.compile_utils import (
    DelegatedTokenizerAttributes,
    DelegatedTokenizerMethods,
)


class CompiledTokenizer(object):
    """A wrapper class around huggingface Tokenizer.

    Includes extension of save_pretrained & load_pretrained methods to specified
    tokenization parameters and a __call__ method that will override kwargs in favour of those
    tokenization parameters. Useful in combination with (neuron-)compiled models, and the
    CompiledModel class with or without the use of transformer Pipelines.
    """

    def __init__(
        self,
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        **tokenization_kwargs: Any
    ):

        self.tokenizer = deepcopy(tokenizer)
        self.tokenization_settings = self.get_tokenization_settings(
            tokenizer, **tokenization_kwargs
        )
        self.compiled = True
        # attach base suite of delegated methods implemented by the hf tokenizer to preserve most
        # of the common methods and simulate subclassig w.r.t available methods
        # self.set_all_delegated_tokenizer_methods(tokenizer)
        # the model_max_length should be set to the max length of the compilation
        self.model_max_length = self.tokenization_settings["max_length"]

    def __getattr__(self, name: str) -> Any:
        """Surfaces selected tokenizer attributes/methods to the CompiledTokenizer instance."""
        if (
            name
            in DelegatedTokenizerMethods.list() + DelegatedTokenizerAttributes.list()
        ):
            attribute = self.tokenizer.__getattribute__(name)
        else:
            attribute = self.__dict__[attribute]

        return attribute

    @classmethod
    def get_tokenization_settings(
        cls,
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        **tokenization_kwargs: Any
    ) -> Dict[str, Any]:
        """Returns tokenizer parameter values.

        Sets some reasonable defaults for the params that define tokenization behaviour, in
        particular the padding and sequence length of the resulting tokenized sequences.
        """
        # ensure constant sequence length of outputs as per
        # https://awsdocs-neuron.readthedocs-hosted.com/en/latest/src/examples/tensorflow/...
        # ...huggingface_bert/...
        # ...huggingface_bert.html#Compile-the-model-into-an-AWS-Neuron-Optimized-Model
        tokenization_settings = {"padding": "max_length", "truncation": True}
        # ensure reasonable defaults
        tokenization_settings["add_special_tokens"] = tokenization_kwargs.pop(
            "add_special_tokens", True
        )
        tokenization_settings["max_length"] = tokenization_kwargs.pop(
            "max_length", tokenizer.model_max_length
        )

        tokenization_settings.update(tokenization_kwargs)

        return tokenization_settings

    @classmethod
    def from_tokenizer(
        cls,
        tokenizer: Union[PreTrainedTokenizer, PreTrainedTokenizerFast],
        **tokenization_kwargs: Any
    ) -> "CompiledTokenizer":
        """Utility method wrapper around the constructor for consistency.

        Args:
            tokenizer: (PreTrainedTokenizer,PreTrainedTokenizerFast): The huggingface tokenizer
                instance to compile.
            **tokenization_kwargs (Any): (optional) Additional keyword arguments that can be handled
                by the `tokenizer` instance's __call__ method. Will automatically be specified when
                calling the resulting CompiledTokenizer's __call__ method. Note that the following
                tokenizer keyword arguments will always be set in a CompiledTokenizer instance to
                ensure tokenization behaviour that is compatible with the constant token length
                requirements of a (neuron-)compiled model:
                    - `padding` = 'max_length'
                    - `truncation` = True
        """
        return CompiledTokenizer(tokenizer=tokenizer, **tokenization_kwargs)

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """Canonic huggingface transformers export method.

        Note:
            Only supports exporting to local file system.

        directory (Path,str): Directory on local file system to export tokenizer artifact to. Will
            be created if it doesnt exist.
        """
        # invoke parent class' instance method
        self.tokenizer.save_pretrained(directory)

        with open(
            os.path.join(directory, "tokenization_settings.json"), "w"
        ) as tokenization_settings_file:
            json.dump(self.tokenization_settings, tokenization_settings_file)

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledTokenizer":
        """Canonic huggingface transformers import method.

        Note:
            Only supports importing from local file system.

        directory (Path,str): Directory on local file system to import tokenizer artifact from.
        """
        # use huggingface utility to read generic tokenizer instance from disk
        tokenizer = AutoTokenizer.from_pretrained(directory)
        # load tokenization settings
        with open(
            os.path.join(directory, "tokenization_settings.json"), "r"
        ) as compilation_specs_file:
            tokenization_settings = json.load(compilation_specs_file)

        return CompiledTokenizer(tokenizer=tokenizer, **tokenization_settings)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Overwrite the tokenizer's __call__ kwargs.

        Makes configured tokenization as per compilation arguments
        the default, i.e. no need to remember the exact padding and length configurations at the
        tokenization state. Also useful when this class is being used inside a CompiledPipeline
        instance. Note that the settings specified in the `tokenization_settings` attribute will
        always be given priority, and will override any arguments that may be re-specified when
        calling this method.
        """
        for tokenization_setting in self.tokenization_settings:
            _ = kwargs.pop(tokenization_setting, None)

        kwargs.update(self.tokenization_settings)

        return self.tokenizer(*args, **kwargs)
