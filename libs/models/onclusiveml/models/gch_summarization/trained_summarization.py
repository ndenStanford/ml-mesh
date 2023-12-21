"""Trained Summarizaiton."""

# Standard Library
import os
from pathlib import Path
from typing import Union

# ML libs
from transformers.pipelines import pipeline

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.preprocess import remove_html, remove_whitespace


logger = get_default_logger(__name__, level=20)


class TrainedSummarization:
    """Class for using trained summarization model."""

    def __init__(
        self,
        trained_summarization_pipeline_en: pipeline,
        trained_summarization_pipeline_frde: pipeline,
        trained_summarization_pipeline_es: pipeline,
        trained_summarization_pipeline_ca: pipeline,
        trained_summarization_pipeline_it: pipeline,
    ):
        self.trained_summarization_pipeline_en = trained_summarization_pipeline_en
        self.trained_summarization_pipeline_frde = trained_summarization_pipeline_frde
        self.trained_summarization_pipeline_es = trained_summarization_pipeline_es
        self.trained_summarization_pipeline_ca = trained_summarization_pipeline_ca
        self.trained_summarization_pipeline_it = trained_summarization_pipeline_it

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "TrainedSummarization":
        """Load trained summarization object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained trained
                summatization pipeline
        Returns:
            TrainedSummarization: The loaded pre-trained TrainedSummarization object
        """
        trained_summarization_pipeline_en = pipeline(
            task="summarization",
            model=os.path.join(directory, "english_summarization"),
            device=0,
        )
        trained_summarization_pipeline_frde = pipeline(
            task="summarization",
            model=os.path.join(directory, "french_german_summarization"),
            device=0,
        )
        trained_summarization_pipeline_es = pipeline(
            task="summarization",
            model=os.path.join(directory, "spanish_summarization"),
            device=0,
        )
        trained_summarization_pipeline_ca = pipeline(
            task="summarization",
            model=os.path.join(directory, "catalan_summarization"),
            device=0,
        )
        trained_summarization_pipeline_it = pipeline(
            task="summarization",
            model=os.path.join(directory, "italian_summarization"),
            device=0,
        )
        return cls(
            trained_summarization_pipeline_en=trained_summarization_pipeline_en,
            trained_summarization_pipeline_frde=trained_summarization_pipeline_frde,
            trained_summarization_pipeline_es=trained_summarization_pipeline_es,
            trained_summarization_pipeline_ca=trained_summarization_pipeline_ca,
            trained_summarization_pipeline_it=trained_summarization_pipeline_it,
        )

    def preprocess(self, text: str) -> str:
        """Preprocess the input text by removing unwanted content inside text and tokenizing.

        Args:
            text (str): Raw input text
        Return:
            str: Cleaned text
        """
        text = remove_html(text)
        text = remove_whitespace(text)

        return text

    def inference(self, inputs: str, language: str) -> str:
        """Generate summaries a document.

        Args:
            inputs (str): Input document
            language: (str) Input article language
        Returns:
            summary (str): summary
        """
        if language == "en":
            pipeline = self.trained_summarization_pipeline_en
        elif language == "fr" or language == "de":
            pipeline = self.trained_summarization_pipeline_frde
        elif language == "es":
            pipeline = self.trained_summarization_pipeline_es
        elif language == "ca":
            pipeline = self.trained_summarization_pipeline_ca
        elif language == "it":
            pipeline = self.trained_summarization_pipeline_it
        else:
            pipeline = self.trained_summarization_pipeline_frde
            logger.info(
                "The input language is not well supported yet, will use the MBART for now"
            )

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
            text (str): The input text to summary
            language (str): The input language

        Returns:
            summary (str):
                summary of the input text
        """
        pre_processed_text = self.preprocess(text)
        summary = self.inference(pre_processed_text, language)
        return summary
