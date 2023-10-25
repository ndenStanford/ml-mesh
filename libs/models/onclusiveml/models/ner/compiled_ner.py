"""Compile NER model."""

# Standard Library
import os
import re
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

# 3rd party libraries
from bs4 import BeautifulSoup

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer


DISTILBERT_SUPPORTED_LANGS = ["ko", "ja"]


class InferenceOutput(NamedTuple):
    """Inference output data structure."""

    entity_type: str
    score: float
    entity_text: str
    start: Optional[int] = None
    end: Optional[int] = None
    sentence_index: Optional[int] = None


class CompiledNER:
    """Class for performing Named Entity Recognition (NER) using neuron compiled NER pipeline."""

    def __init__(
        self,
        compiled_ner_pipeline_base: CompiledPipeline,
        compiled_ner_pipeline_kj: CompiledPipeline,
    ):
        """Initalize the CompiledNER object.

        Args:
            compiled_ner_pipeline_base (CompiledPipeline): The compiled NER pipline used for
                inference
            compiled_ner_pipeline_kj (CompiledPipeline): The compiled NER pipline used for
                inference for korean and japanese
        """
        self.compiled_ner_pipeline_base = compiled_ner_pipeline_base
        self.compiled_ner_pipeline_kj = compiled_ner_pipeline_kj
        # Initialise sentence tokenizer
        self.sentence_tokenizer = SentenceTokenizer()

    def save_pretrained(self, directory: Union[Path, str]) -> None:
        """Save compiled NER pipeline to specified directory.

        Args:
            directory (Union[Path, str]): Directory to save the compiled NER pipeline
        """
        self.compiled_ner_pipeline_base.save_pretrained(
            os.path.join(directory, "compiled_ner_pipeline_base")
        )
        self.compiled_ner_pipeline_kj.save_pretrained(
            os.path.join(directory, "compiled_ner_pipeline_kj")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledNER":
        """Load compiledNER object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                ner pipeline
        Returns:
            CompiledNER: The loaded pre-trained CompiledNER object
        """
        compiled_ner_pipeline_base = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_ner_pipeline_base")
        )
        compiled_ner_pipeline_kj = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_ner_pipeline_kj")
        )

        return cls(
            compiled_ner_pipeline_base=compiled_ner_pipeline_base,
            compiled_ner_pipeline_kj=compiled_ner_pipeline_kj,
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

    def sentence_tokenize(self, sentences: List[str], language: str) -> List[str]:
        """Sentence tokenization.

        Args:
            sentences (List[str]): Input sentences.
            language (str): Input sentences language.

        Return:
            List[List[str]]: Tokenized sentences
        """
        list_sentences = [
            self.sentence_tokenizer.tokenize(content=sentence, language=language)[
                "sentences"
            ]
            for sentence in sentences
        ]

        return list_sentences

    def preprocess(self, sentences: List[str], language: str) -> List[str]:
        """Preprocess the input sentences by removing unwanted content inside text and tokenizing.

        Args:
            sentences (List[str]): Input sentences
            language (str): Input sentences language

        Return:
            List[List[str]]: Tokenized sentences
        """
        sentences = [self.remove_html(sentence) for sentence in sentences]
        sentences = [self.remove_whitespace(sentence) for sentence in sentences]
        return self.sentence_tokenize(sentences, language)

    def inference(
        self, sentences: List[str], language: str
    ) -> List[List[InferenceOutput]]:
        """Perform NER inference on a list of sentences.

        Args:
            sentences (List[str]): list of sentences
            language: (str) language of given sentences

        Returns:
            InferenceOutput: List of lists of NER predictions which has the attributes:
                - entity_type (str): entity type
                - score (float): probability of given entity
                - entity_text (str): targeted word for given entity
                - start (int): starting position of word
                - end (int): ending position of word
        """
        if language in DISTILBERT_SUPPORTED_LANGS:
            entities = self.compiled_ner_pipeline_kj(sentences)
        else:
            entities = self.compiled_ner_pipeline_base(sentences)
        for sublist in entities:
            for dictionary in sublist:
                dictionary.pop("index", None)
                dictionary["entity_type"] = dictionary.pop("entity")
                dictionary["entity_text"] = dictionary.pop("word")

        return [
            [InferenceOutput(**dictionary) for dictionary in sublist]
            for sublist in entities
        ]

    def compute_moving_average(self, scores: List[float]) -> float:
        """Compute the moving average of a list of scores.

        Args:
            scores (List[float]): List of scores for which to compute the moving average

        Returns:
            float: The computed moving average
        """
        return sum(scores) / len(scores)

    def postprocess(
        self, output: List[List[InferenceOutput]]
    ) -> List[List[InferenceOutput]]:
        """Postprocess NER labels to merge contiguous entities and compute scores.

        Args:
            output (List[List[InferenceOutput]]): List of lists of NER predictions
                which has the attributes:
                    - entity_type (str): entity type
                    - score (float): probability of given entity
                    - entity_text (str): targeted word for given entity
                    - start (int): starting position of word
                    - end (int): ending position of word

        Returns:
            List[List[InferenceOutput]]: List of extracted named
                entities in dictionary format.
        """
        output_list: List[
            List[InferenceOutput]
        ] = []  # List to store the postprocessed NER labels

        sentence_index = 0  # Initialize sentence index for tracking
        # Loop through each sublist of NER labels (one sublist per sentence)
        for sublist in output:
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
                entity = dictionary.entity_type
                score = dictionary.score
                word = dictionary.entity_text
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
                            InferenceOutput(
                                entity_type=current_entity[2:],
                                score=float(
                                    self.compute_moving_average(current_score_list)
                                    if len(current_score_list) > 1
                                    else current_score_list[0]
                                ),
                                sentence_index=sentence_index,
                                entity_text=current_word,
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
                    InferenceOutput(
                        entity_type=current_entity[2:],
                        score=float(
                            self.compute_moving_average(current_score_list)
                            if len(current_score_list) > 1
                            else current_score_list[0]
                        ),
                        sentence_index=sentence_index,
                        entity_text=current_word,
                        start=current_start,
                        end=current_end,
                    )
                )
            # Append the merged_sublist for the current sentence to the output_list
            output_list.append(merged_sublist)
            # Increment the sentence index for the next iteration
            sentence_index += 1

        return output_list

    def __call__(
        self, sentences: List[str], language: str
    ) -> List[List[InferenceOutput]]:
        """Extract named entities from input sentence using NER.

        Args:
            sentences (str): The input sentences to extract entities from
            language (str): input sentences language
        Returns:
            List[List[InferenceOutput]]: List of extracted named
                entities in dictionary format.
        """
        list_sentences = self.preprocess(sentences, language)
        ner_labels = self.inference(list_sentences, language)
        entities = self.postprocess(ner_labels)

        return entities
