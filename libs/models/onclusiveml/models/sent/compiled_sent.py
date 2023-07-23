# Standard Library
import os
import re
import string
from pathlib import Path
from typing import List, Union

# 3rd party libraries
import regex
from bs4 import BeautifulSoup

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer


class CompiledSent:
    """Class for performing sentiment analysis using neuron compiled Sent pipeline"""

    def __init__(
        self,
        compiled_sent_pipeline: CompiledPipeline,
    ):
        """
        Initalize the CompiledSent object.
        Args:
            compiled_sent_pipeline (CompiledPipeline): The compiled Sent pipline used for inference
        """
        self.compiled_sent_pipeline = compiled_sent_pipeline
        self.unicode_strp = regex.compile(r"\p{P}")
        self.NUM_LABELS = 3
        self.MAX_SEQ_LENGTH = 128
        self.MAX_BATCH_SIZE = 6
        self.device: str = "cpu"

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """
        Save compiled Sent pipeline to specified directory
        Args:
            Directory (Union[Path, str]): Directory to save the compiled Sent pipeline
        """
        self.compiled_sent_pipeline.save_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledSent":
        """
        Load compiledSent object from specfied directory
        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                sent pipeline
        Returns:
            CompiledSent: The loaded pre-trained CompiledSent object
        """
        compiled_sent_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

        return cls(
            compiled_sent_pipeline=compiled_sent_pipeline,
        )

    def remove_html(self, text: str) -> str:
        """
        Remove HTML tags from input text
        Args:
            text (str): Input text
        Returns:
            str: Text with HTML tags removed
        """
        text = BeautifulSoup(text, "html.parser").text
        return text

    def remove_whitespace(self, text: str) -> str:
        """
        Remove extra white spaces from input text."
        Args:
            text (str): Input text
        Returns:
            str: Text with extra whitespaces removed
        """

        text = re.sub(r"\s+", " ", text)
        return text

    def preprocess(self, sentences: str) -> List[str]:
        """
        Preprocess the input sentences by removing unwanted content inside text and tokenizing

        Args:
            sentences (str): Input sentences
        Return:
            List[str]: Tokenized sentences
        """
        sentences = self.remove_html(sentences)
        sentences = self.remove_whitespace(sentences)
        tokenizer = SentenceTokenizer()
        list_sentences = tokenizer.tokenize(content=sentences)[
            "sentences"
        ]  # default is english
        # very short sentences are likely somehow wrong
        list_sentences = [sentence for sentence in list_sentences if len(sentence) > 5]
        # Additional separation, need to check if this is needed
        list_sentences = [
            self.unicode_strp.sub("", sentence) for sentence in list_sentences
        ]
        list_sentences = [
            sentence.translate(str.maketrans("", "", string.punctuation))
            for sentence in list_sentences
        ]

        return list_sentences
