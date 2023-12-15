"""Compiled topic."""

# Standard Library
from pathlib import Path
from typing import Tuple, Union

# 3rd party libraries
from bertopic import BERTopic

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.clean import clean


logger = get_default_logger(__name__, level=20)


class TrainedTopic:
    """Class for performing topic detection using trained topic model."""

    def __init__(
        self,
        trained_topic_model: BERTopic,
    ):
        self.trained_topic_model = trained_topic_model

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "TrainedTopic":
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

    def preprocess(self, sentences: str) -> str:
        """Preprocess the input sentences by removing unwanted content inside text and tokenizing.

        Args:
            sentences (str): Input sentences
        Return:
            List[str]: Cleaned sentences
        """
        sentences = clean.remove_html(sentences)
        sentences = clean.remove_whitespace(sentences)

        return sentences

    def inference(self, text: str) -> Tuple:
        """Detect topic of the input text.

        Args:
            text (str): Input text for topic detection.

        Returns:
            topic_representaion (NDArray): List of keywords for topic representation.
        """
        self.inputs = text

        topic_id, prob = self.trained_topic_model.transform(text)
        topic_representation = self.trained_topic_model.get_topic(int(topic_id))

        return (topic_id, topic_representation)

    def __call__(
        self,
        text: str,
    ) -> Tuple:
        """Topic detection of input text.

        Args:
            text (str): The input text to detect topic.

        Returns:
            topic_id (str):
                ID of the predicted topic.
        """
        pre_processed_text = self.preprocess(text)
        topic_id, topic_representation = self.inference(pre_processed_text)
        return (topic_id, topic_representation)
