"""Compiled topic."""

# Standard Library
import os
import re
from pathlib import Path
from typing import Union

# 3rd party libraries
from bs4 import BeautifulSoup

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=20)


class TrainedSummarization:
    """Class for using trained summarization model."""

    def __init__(
        self,
        compiled_summarization_pipeline_en: CompiledPipeline,
        compiled_summarization_pipeline_frde: CompiledPipeline,
        compiled_summarization_pipeline_es: CompiledPipeline,
        compiled_summarization_pipeline_ca: CompiledPipeline,
        compiled_summarization_pipeline_it: CompiledPipeline,
    ):
        self.compiled_summarization_pipeline_en = compiled_summarization_pipeline_en
        self.compiled_summarization_pipeline_frde = compiled_summarization_pipeline_frde
        self.compiled_summarization_pipeline_es = compiled_summarization_pipeline_es
        self.compiled_summarization_pipeline_ca = compiled_summarization_pipeline_ca
        self.compiled_summarization_pipeline_it = compiled_summarization_pipeline_it

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "TrainedSummarization":
        """Load compiled summarization object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                sent pipeline
        Returns:
            CompiledSummarization: The loaded pre-trained CompiledSummarization object
        """
        compiled_summarization_pipeline_en = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_summarizaton_pipeline_en")
        )
        compiled_summarization_pipeline_frde = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_summarizaton_pipeline_frde")
        )
        compiled_summarization_pipeline_es = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_summarizaton_pipeline_es")
        )
        compiled_summarization_pipeline_ca = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_summarizaton_pipeline_ca")
        )
        compiled_summarization_pipeline_it = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_summarizaton_pipeline_it")
        )
        return cls(
            compiled_summarization_pipeline_en=compiled_summarization_pipeline_en,
            compiled_summarization_pipeline_frde=compiled_summarization_pipeline_frde,
            compiled_summarization_pipeline_es=compiled_summarization_pipeline_es,
            compiled_summarization_pipeline_ca=compiled_summarization_pipeline_ca,
            compiled_summarization_pipeline_it=compiled_summarization_pipeline_it,
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

    def preprocess(self, sentences: str) -> str:
        """Preprocess the input sentences by removing unwanted content inside text and tokenizing.

        Args:
            sentences (str): Input sentences
        Return:
            List[str]: Cleaned sentences
        """
        sentences = self.remove_html(sentences)
        sentences = self.remove_whitespace(sentences)

        return sentences

    def inference(self, inputs: str, language: str) -> str:
        """Generate summaries a document.

        Args:
            inputs (str): Input document
            language: (str) Input article language
        Returns:
            summary (str): summary
        """
        if language == "en":
            pipeline = self.compiled_summarization_pipeline_en
        elif language == "fr" or language == "de":
            pipeline = self.compiled_summarization_pipeline_frde
        elif language == "es":
            pipeline = self.compiled_summarization_pipeline_es
        elif language == "ca":
            pipeline = self.compiled_summarization_pipeline_ca
        elif language == "it":
            pipeline = self.compiled_summarization_pipeline_it

        output = pipeline(
            inputs,
            min_length=32,
            max_length=128,
            num_beams=1,
        )

        summary = output[0]["summary_text"]
        return summary

    def __call__(
        self,
        text: str,
        language: str,
    ) -> str:
        """Topic detection of input text.

        Args:
            text (str): The input text to detect topic.

        Returns:
            topic_id (str):
                ID of the predicted topic.
        """
        pre_processed_text = self.preprocess(text)
        summary = self.inference(pre_processed_text, language=language)
        return summary
