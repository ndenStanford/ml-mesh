"""Compiled topic."""

# Standard Library
import re
from pathlib import Path
from typing import Union

# 3rd party libraries
from bertopic import BERTopic
from bs4 import BeautifulSoup
from nptyping import NDArray

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=20)


class TrainedTopic:
    """Class for performing topic detection using trained topic model."""

    def __init__(
        self,
        trained_topic_model: BERTopic,
    ):
        """Initalize the TrainedTopic object."""
        self.embedding_model = (
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.trained_topic_model = trained_topic_model

    @classmethod
    def load_trained(cls, directory: Union[Path, str]) -> "TrainedTopic":
        """Load TrainedTopic object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path containing the trained
                topic model
        Returns:
            TrainedTopic: The loaded trained Topic object
        """
        trained_topic_model = BERTopic.load(directory)

        return cls(
            trained_topic_model=trained_topic_model,
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

    def inference(self, text: str) -> NDArray:
        """Detect topic of the input text.

        Args:
            text (str): Input text for topic detection.

        Returns:
            topic_representaion (NDArray): List of keywords for topic representation.
        """
        self.inputs = text

        topic_id, prob = self.trained_topic_model.transform(text)
        topic = self.trained_topic_model.get_topic(int(topic_id))

        return topic_id, topic

    def __call__(
        self,
        text: str,
    ) -> str:
        """Topic detection of input text.

        Args:
            text (str): The input text to detect topic.

        Returns:
            topic_id (str):
                ID of the predicted topic.
        """
        pre_processed_text = self.preprocess(text)
        topic_id = self.inference(pre_processed_text)
        return topic_id
