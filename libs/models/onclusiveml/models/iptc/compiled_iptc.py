"""Compiled iptc."""

# Standard Library
import os
import re
from pathlib import Path
from typing import List, Union

# ML libs
import torch

# 3rd party libraries
import regex
from bs4 import BeautifulSoup
from nptyping import NDArray
from pydantic import BaseModel

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import get_default_logger
from onclusiveml.models.iptc.class_dict import CLASS_DICT_FIRST


logger = get_default_logger(__name__, level=20)


class PostProcessOutput(BaseModel):
    """output data structure."""

    label: str
    score: float


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
        self.id2label = CLASS_DICT_FIRST["root"]
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

    def remove_html(self, text: str) -> str:
        """Remove HTML tags from input text.

        Args:
            text (str): Input text
        Returns:
            str: Text with HTML tags removed
        """
        text = BeautifulSoup(text, "html.parser").text
        return text

    def remove_whitespace(self, text: str) -> str:
        """Remove extra white spaces from input text.

        Args:
            text (str): Input text
        Returns:
            str: Text with extra whitespaces removed
        """
        text = re.sub(r"\s+", " ", text)
        return text

    def preprocess(self, input_data: str) -> str:
        """Preprocess the input.

        Args:
            input_data (str): Input data
        Return:
            inputdata(str): input data
        """
        input_data = self.remove_html(input_data)
        input_data = self.remove_whitespace(input_data)
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
        iptc_probs_arr: NDArray = (
            torch.nn.functional.softmax(res["logits"]).detach().numpy()[0]
        )

        return iptc_probs_arr

    def postprocess(self, probs: NDArray) -> List[PostProcessOutput]:
        """Postprocess the probabilities to output structured data.

        Args:
            probs (NDArray): Array of iptc probabilities.

        Returns:
            List[PostProcessOutput]: A list of PostProcessOutput objects with predicted
            label and score.
        """
        predictions = [
            PostProcessOutput(label=self.id2label[index], score=round(float(prob), 4))
            for index, prob in enumerate(probs)
        ]
        return sorted(predictions, key=lambda x: x.score, reverse=True)

    def __call__(self, input_data: str) -> List[PostProcessOutput]:
        """IPTC detection for input content.

        Args:
            input_data (str): The input content to be analyzed.

        Returns:
            List[PostProcessOutput]: A list of PostProcessOutput objects representing
            the IPTC analysis results.
        """
        content = self.preprocess(input_data)
        iptc_probs = self.inference(content)
        return self.postprocess(iptc_probs)