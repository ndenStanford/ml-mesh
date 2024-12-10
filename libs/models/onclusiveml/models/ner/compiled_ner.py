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
        res = [
            [
                self.compiled_ner_pipeline_base(sentence, aggregation_strategy="simple")
                for sentence in doc_sentences
            ]
            for doc_sentences in sent_tokenized_documents
        ]
        processed_results = []
        for doc_idx, doc in enumerate(res):
            doc_entities = []
            for sent_idx, sent_entities in enumerate(doc):
                sentence = sent_tokenized_documents[doc_idx][sent_idx]
                for entity in sent_entities:
                    start_pos = entity["start"]
                    if language not in ["ja", "zh"]:
                        # To check if the entity is following a space that will cause the start_pos shift
                        if start_pos > 0 and sentence[start_pos].isspace():
                            start_pos += 1
                    doc_entities.append(
                        InferenceOutput(
                            entity_type=entity["entity_group"],
                            score=entity["score"],
                            entity_text=entity["word"],
                            start=start_pos,
                            end=entity["end"],
                            sentence_index=sent_idx,
                        )
                    )
            processed_results.append([doc_entities])

        return processed_results

    def postprocess(
        self, ner_predictions: List[List[InferenceOutput]]
    ) -> List[List[InferenceOutput]]:
        """Filter out invalid or unwanted entities from NER predictions.

        Args:
            ner_predictions: Nested list of NER predictions as InferenceOutput objects

        Returns:
            List[List[InferenceOutput]]: Filtered list of valid entities, excluding:
                - Entities with same start and end positions
                - Empty entity text
                - Single characters: "'", "-", "_"
        """
        converted_entities = []
        for entities_list in ner_predictions:
            for entity in entities_list:
                if (
                    entity.start != entity.end
                    and len(entity.entity_text) > 0
                    and entity.entity_text not in ["'", "-", "_"]
                ):
                    converted_entities.append(entity)
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
