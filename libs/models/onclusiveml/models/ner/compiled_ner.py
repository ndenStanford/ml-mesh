"""Compile NER model."""

# Standard Library
import os
from pathlib import Path
from typing import List, NamedTuple, Optional, Union

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.nlp import preprocess
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer


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

    def __init__(self, compiled_ner_pipeline_base: CompiledPipeline):
        """Initalize the CompiledNER object.

        Args:
            compiled_ner_pipeline_base (CompiledPipeline): The compiled NER pipline used for
                inference
            compiled_ner_pipeline_korean_and_japanese (CompiledPipeline): The compiled NER pipline used for
                inference for korean and japanese
        """
        self.compiled_ner_pipeline_base = compiled_ner_pipeline_base
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
            os.path.join(directory, "compiled_ner_pipeline_base"),
        )

        return cls(compiled_ner_pipeline_base=compiled_ner_pipeline_base)

    def sentence_tokenize(self, documents: List[str], language: str) -> List[List[str]]:
        """Sentence tokenization.

        Args:
            documents (List[str]): List of documents.
            language (str): Input sentences language.

        Return:
            List[List[str]]: Tokenized sentences for each document as a list
        """
        list_sentences = [
            self.sentence_tokenizer.tokenize(content=doc, language=language)[
                "sentences"
            ]
            for doc in documents
        ]

        return list_sentences

    def preprocess(self, documents: List[str], language: str) -> List[List[str]]:
        """Preprocess the list of documents by removing unwanted text and tokenizing.

        Args:
            documents (List[str]): List of documents
            language (str): Input sentences language

        Return:
            List[List[str]]: Tokenized sentences, each sublist are tokenized strings for a document
        """
        documents = [preprocess.remove_html(doc) for doc in documents]
        documents = [preprocess.remove_whitespace(doc) for doc in documents]
        return self.sentence_tokenize(documents, language)

    def inference(
        self, sent_tokenized_documents: List[List[str]], language: str
    ) -> List[List[InferenceOutput]]:
        """Perform NER inference on a list of documents.

        Args:
            sent_tokenized_documents (List[List[str]]): Nested list of tokenized sentence where
                each sublist represent a document
            language: (str) Input sentences language

        Returns:
            InferenceOutput: Nested list of NER predictions where each sublist represents entities
                of a document. Attributes:
                - entity_type (str): entity type
                - score (float): probability of given entity
                - entity_text (str): targeted word for given entity
                - start (int): starting position of word
                - end (int): ending position of word
        """
        res = list(map(self.compiled_ner_pipeline_base, sent_tokenized_documents))
        # results are in nested list of entities where each sublist represents a doc
        for doc in res:
            for entities_list in doc:
                for dictionary in entities_list:
                    dictionary.pop("index", None)
                    dictionary["entity_type"] = dictionary.pop("entity")
                    dictionary["entity_text"] = dictionary.pop("word")
        return [
            [
                [InferenceOutput(**dictionary) for dictionary in entities_list]
                for entities_list in docs
            ]
            for docs in res
        ]

    def compute_average(self, scores: List[float]) -> float:
        """Compute the average of a list of scores.

        Args:
            scores (List[float]): List of scores for

        Returns:
            float: The computed average
        """
        return sum(scores) / len(scores)

    def postprocess(
        self, ner_predictions: List[List[InferenceOutput]]
    ) -> List[List[InferenceOutput]]:
        """Postprocess nested list of NER predictions by aggregating BIO tags.

        Args:
            ner_predictions: List[List[InferenceOutput]]: Nested list of NER predictions

        Returns:
            List[List[InferenceOutput]]: Post processed NER predictions
        """
        flattened_entities = []
        # Flatten the predictions and add sentence index
        for sentence_idx, sentence_entities in enumerate(ner_predictions):
            for entity in sentence_entities:
                # Convert NamedTuple to dictionary and add sentence_index
                entity_dict = entity._asdict()
                entity_dict["sentence_index"] = sentence_idx
                flattened_entities.append(entity_dict)

        # Merge entities based on B- and I- prefix
        merged_entities = []
        current_entity = None
        current_scores = []  # Track scores for true average calculation

        for entity in flattened_entities:
            # Check if it's a beginning of a new entity (B- prefix) or there is no current entity
            if entity["entity_type"].startswith("B-") or current_entity is None:
                if current_entity:  # If there's an ongoing entity, finalize it
                    current_entity["score"] = self.compute_average(
                        current_scores
                    )  # Use true average
                    merged_entities.append(current_entity)
                # Start a new entity
                current_entity = entity.copy()
                current_scores = [entity["score"]]
            elif entity["entity_type"].startswith("I-") and current_entity:
                # Merge with the current entity
                current_entity["entity_text"] += entity["entity_text"]
                current_entity["end"] = entity["end"]
                current_scores.append(entity["score"])  # Add the new score to the list
            else:
                # If the entity type is neither B- nor I-, consider it as a new entity
                if current_entity:
                    current_entity["score"] = self.compute_average(current_scores)
                    merged_entities.append(current_entity)
                current_entity = entity.copy()
                current_scores = [entity["score"]]

        # Append the last entity if any
        if current_entity:
            current_entity["score"] = self.compute_average(current_scores)
            merged_entities.append(current_entity)

        # Post-process merged entities
        converted_entities = []
        for entity in merged_entities:
            entity["entity_type"] = entity["entity_type"][
                2:
            ]  # Remove prefix (e.g., "B-", "I-")
            if entity["entity_text"][0] == "▁":
                entity["start"] += (
                    1 if entity["start"] != 0 else 0
                )  # Adjust start position (account for _ offset) if mid-sentence
            entity["entity_text"] = entity["entity_text"].strip("▁").replace("▁", " ")
            if (
                entity["start"] != entity["end"]
                and len(entity["entity_text"]) > 0
                and entity["entity_text"] not in ["'", "-", "_", "▁"]
            ):
                converted_entities.append(InferenceOutput(**entity))

        return converted_entities

    def __call__(
        self, documents: List[str], language: str
    ) -> List[List[InferenceOutput]]:
        """Extract named entities from input sentence using NER.

        Args:
            documents (List[str]): List of documents to extract entities from
            language (str): input sentences language
        Returns:
            List[List[InferenceOutput]]: List of extracted named
                entities in dictionary format.
        """
        sent_tokenized_documents = self.preprocess(documents, language)
        ner_labels = self.inference(sent_tokenized_documents, language)
        entities = list(map(self.postprocess, ner_labels))
        return entities
