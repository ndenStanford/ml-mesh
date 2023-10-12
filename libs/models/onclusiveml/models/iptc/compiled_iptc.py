"""Compiled iptc."""

# Standard Library
import os
from pathlib import Path
from typing import Any, Dict, Union

# 3rd party libraries
import regex
from nptyping import NDArray

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.iptc.class_dict import CLASS_DICT


logger = get_default_logger(__name__, level=20)


class CompiledIPTC:
    """Class for performing iptc using neuron compiled IPTC pipeline."""

    def __init__(
        self,
        compiled_iptc_pipeline: CompiledPipeline,
    ):
        """Initalize the CompiledIPTC object.

        Args:
            compiled_iptc_pipeline (CompiledPipeline): The compiled iptc pipline used for inference
        """
        self.compiled_iptc_pipeline = compiled_iptc_pipeline
        self.unicode_strp = regex.compile(r"\p{P}")
        self.id2label = CLASS_DICT["root"]
        self.NUM_LABELS = len(self.id2label)
        self.MAX_SEQ_LENGTH = (
            compiled_iptc_pipeline.compiled_pipeline.model.compilation_specs[
                "tracing__max_length"
            ]
        )
        self.MAX_BATCH_SIZE = (
            compiled_iptc_pipeline.compiled_pipeline.model.compilation_specs[
                "tracing__batch_size"
            ]
        )
        self.device: str = "cpu"

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """Save compiled iptc pipeline to specified directory.

        Args:
            directory (Union[Path, str]): Directory to save the compiled iptc pipeline
        """
        self.compiled_iptc_pipeline.save_pretrained(
            os.path.join(directory, "compiled_iptc_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledIPTC":
        """Load compilediptc object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                iptc pipeline
        Returns:
            CompiledIPTC: The loaded pre-trained CompiledIPTC object
        """
        compiled_iptc_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_iptc_pipeline")
        )

        return cls(
            compiled_iptc_pipeline=compiled_iptc_pipeline,
        )

    def preprocess(self, input_data: str) -> str:
        """Preprocess the input.

        Args:
            input_data (str): Input data
        Return:
            inputdata(str): input data
        """
        return input_data

    def inference(self, content: str) -> NDArray:
        """Compute iptc probability.

        Args:
            content (str): Input content
        Returns:
            iptc_probs (NDArray): List of iptc probability
        """
        self.inputs = self.compiled_iptc_pipeline.tokenizer(
            content,
            return_tensors="pt",
        )

        res = self.compiled_iptc_pipeline.model(**self.inputs)
        iptc_probs_arr: NDArray = res["logits"].clone().detach().numpy().astype(float)

        assert iptc_probs_arr.shape[0] == 1
        return iptc_probs_arr

    def postprocess(self, probs: NDArray) -> Dict[Any, float]:
        """Postprecess the probs.

        Args:
            probs (NDArray): List of iptc probability
        Return:
            result(dict): predict label for iptc
        """
        prediction_dict = {
            self.id2label[index]: round(float(prob), 4)
            for index, prob in enumerate(probs)
        }
        return prediction_dict

    def extract_iptc(self, input_data: str) -> Dict[Any, float]:
        """Iptc detection of input content.

        Args:
            input_data (str): The input content
        Returns:
            iptc_output (Dict[str, Union[float, str, List]]):
                Extracted iptc in dictionary format
        """
        content = self.preprocess(input_data)
        iptc_prob_list = self.inference(content)
        iptc_output = self.postprocess(iptc_prob_list)
        return iptc_output
