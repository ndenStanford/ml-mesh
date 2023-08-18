# Standard Library
import os
import re
from pathlib import Path
from typing import List, Union

# 3rd party libraries
from bs4 import BeautifulSoup

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.models.ner.settings import (
    InferenceOutput,
    PostprocessOutput,
    PostprocessOutputNoPos,
)
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer


class CompiledNER:
    """Class for performing Named Entity Recognition (NER) using neuron compiled NER pipeline"""

    def __init__(
        self,
        compiled_ner_pipeline: CompiledPipeline,
    ):
        """
        Initalize the CompiledNER object.
        Args:
            compiled_ner_pipeline (CompiledPipeline): The compiled NER pipline used for inference
        """
        self.compiled_ner_pipeline = compiled_ner_pipeline
        # Initialise sentence tokenizer
        self.sentence_tokenizer = SentenceTokenizer()

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """
        Save compiled NER pipeline to specified directory
        Args:
            Directory (Union[Path, str]): Directory to save the compiled NER pipeline
        """
        self.compiled_ner_pipeline.save_pretrained(
            os.path.join(directory, "compiled_ner_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledNER":
        """
        Load compiledNER object from specfied directory
        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                ner pipeline
        Returns:
            CompiledNER: The loaded pre-trained CompiledNER object
        """
        compiled_ner_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_ner_pipeline")
        )

        return cls(
            compiled_ner_pipeline=compiled_ner_pipeline,
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

    def sentence_tokenize(self, sentences: str, language: str) -> List[str]:
        list_sentences = self.sentence_tokenizer.tokenize(
            content=sentences, language=language
        )["sentences"]
        # Filter out very short sentences as they likely be incorrect
        list_sentences = [sentence for sentence in list_sentences if len(sentence) > 5]
        return list_sentences

    def preprocess(self, sentences: str, language: str) -> List[str]:
        """
        Preprocess the input sentences by removing unwanted content inside text and tokenizing

        Args:
            sentences (str): Input sentences
        Return:
            List[str]: Tokenized sentences
        """
        sentences = self.remove_html(sentences)
        sentences = self.remove_whitespace(sentences)
        list_sentences = self.sentence_tokenize(sentences, language)
        return list_sentences

    def inference(self, sentences: List[str]) -> InferenceOutput:
        """
        Perform NER inference on a list of sentences.

        Args:
            sentences (List[str]): list of sentences

        Returns:
            InferenceOutput: List of lists of NER predictions which has the attributes:
                - entity (str): entity type
                - score (float): probability of given entity
                - word (str): targeted word for given entity
                - start (int): starting position of word
                - end (int): ending position of word
        """
        entities = self.compiled_ner_pipeline(sentences)
        for sublist in entities:
            for dictionary in sublist:
                dictionary.pop("index", None)

        return InferenceOutput(ner_labels=entities)

    def compute_moving_average(self, scores: List[float]) -> float:
        """
        Compute the moving average of a list of scores.

        Args:
            scores (List[float]): List of scores for which to compute the moving average

        Returns:
            float: The computed moving average
        """
        return sum(scores) / len(scores)

    def postprocess(
        self, ner_labels: InferenceOutput, return_pos: bool
    ) -> Union[List[PostprocessOutput], List[PostprocessOutputNoPos]]:
        """
        Postprocess NER labels to merge contiguous entities and compute scores

        Args:
            InferenceOutput: List of lists of NER predictions which has the attributes:
                - entity (str): entity type
                - score (float): probability of given entity
                - word (str): targeted word for given entity
                - start (int): starting position of word
                - end (int): ending position of word
            return_pos (bool): Flag indicating whether to return positional information

        Returns:
            Union[List[PostprocessOutput], List[PostprocessOutputNoPos]]: List of extracted named
                entities in dictionary format.
                PostprocessOutput has attributes:
                    - entity (str): entity type
                    - score (float): probability of given entity
                    - word (str): targeted word for given entity
                    - start (int): starting position of word
                    - end (int): ending position of word
                    - sentence index (int): sentence location of word

                PostprocessOutputNoPos has attributes:
                    - entity (str): entity type
                    - score (float): probability of given entity
                    - word (str): targeted word for given entity
                    - start (int): starting position of word
        """
        output_list: List[
            PostprocessOutput
        ] = []  # List to store the postprocessed NER labels
        sentence_index = 0  # Initialize sentence index for tracking
        # Loop through each sublist of NER labels (one sublist per sentence)
        for sublist in ner_labels.ner_labels:
            merged_sublist = (
                []
            )  # List to store merged contiguous entities for the current sentence
            current_entity = (
                None  # init variables for tracking current entity and properties
            )
            current_score_list = []  # List to store scores of contiguous entities
            current_word = ""  # Initialise variable for tracking current merged word
            current_start = (
                None  # Initalize variable for tracking start pos of merged entity
            )
            current_end = (
                None  # Initalize variable for tracking end pos of merged entity
            )
            # loop through each dictionary (NER label) in the sublist
            for dictionary in sublist:
                entity = dictionary.entity
                score = dictionary.score
                word = dictionary.word
                start = dictionary.start
                end = dictionary.end
                # Check if the 'end' value of the current entity matches the 'start' value
                # of the next entity
                if current_end == start:
                    # Append the next entity if the 'end' value is the same as the 'start'
                    # value of the next entity.
                    current_score_list.append(score)
                    current_word += (
                        "" + word[2:]
                    )  # merge words while skipping the 'B-' or 'I-' prefix
                    current_end = end
                # Check if the current entity is a continuation of the previouss entity
                elif entity.startswith("I-"):
                    if current_entity is not None:
                        current_score_list.append(score)  # type: ignore[unreachable]
                        current_word += " " + word
                        current_end = end
                # Check if the current entity is the beginning of a new entity
                elif entity.startswith("B-"):
                    if current_entity is not None:
                        # Append the merged entity with computed score to the merged_sublist
                        merged_sublist.append(  # type: ignore[unreachable]
                            PostprocessOutput(
                                entity=current_entity[2:],
                                score=float(
                                    self.compute_moving_average(current_score_list)
                                    if len(current_score_list) > 1
                                    else current_score_list[0]
                                ),
                                sentence_index=sentence_index,
                                word=current_word,
                                start=current_start,
                                end=current_end,
                            )
                        )
                    # update the current entity
                    current_entity = entity
                    current_score_list = [score]
                    current_word = word
                    current_start = start
                    current_end = end
            # Check if there is an unprocessed entity left at the end of the sublist
            if current_entity is not None:
                # Append the merged entity with computed score to the merged_sublist
                merged_sublist.append(
                    PostprocessOutput(
                        entity=current_entity[2:],
                        score=float(
                            self.compute_moving_average(current_score_list)
                            if len(current_score_list) > 1
                            else current_score_list[0]
                        ),
                        sentence_index=sentence_index,
                        word=current_word,
                        start=current_start,
                        end=current_end,
                    )
                )
            # Append the merged_sublist for the current sentence to the output_list
            output_list.append(merged_sublist)
            # Increment the sentence index for the next iteration
            sentence_index += 1
        # Flatten the output list
        output_list = [item for sublist in output_list for item in sublist]

        # Remove start and end key from output if we do not want to have the word positions
        if not return_pos:
            output_list_no_pos = []
            for ent in output_list:
                output_list_no_pos.append(
                    PostprocessOutputNoPos(**ent.dict(exclude={"start", "end"}))
                )
            return output_list_no_pos
        return output_list

    def extract_entities(
        self, sentences: str, language: str, return_pos: bool
    ) -> Union[List[PostprocessOutput], List[PostprocessOutputNoPos]]:
        """
        Extract named entities from input sentence using NER
        Args:
            sentences (str): The input sentences to extract entities from
            return_pos (bool): Flag indiciating whether to return positional information in the
                output
        Returns:
            Union[List[PostprocessOutput], List[PostprocessOutputNoPos]]: List of extracted named
                entities in dictionary format.
                PostprocessOutput has attributes:
                    - entity (str): entity type
                    - score (float): probability of given entity
                    - word (str): targeted word for given entity
                    - start (int): starting position of word
                    - end (int): ending position of word
                    - sentence index (int): sentence location of word

                PostprocessOutputNoPos has attributes:
                    - entity (str): entity type
                    - score (float): probability of given entity
                    - word (str): targeted word for given entity
                    - start (int): starting position of word
        """
        list_sentences = self.preprocess(sentences, language)
        ner_labels = self.inference(list_sentences)
        entities = self.postprocess(ner_labels, return_pos)
        return entities
