# Standard Library
import os
import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple, Union

# ML libs
import torch
from torch.utils.data import DataLoader

# 3rd party libraries
from bs4 import BeautifulSoup

# Internal libraries
from onclusiveml.compile import CompiledPipeline
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
        self.id2label: Dict[int, str] = {
            0: "O",
            1: "B-MISC",
            2: "I-MISC",
            3: "B-PER",
            4: "I-PER",
            5: "B-ORG",
            6: "I-ORG",
            7: "B-LOC",
            8: "I-LOC",
        }
        self.MAX_BATCH_SIZE: int = 6
        self.DUMMY_SENTENCE: str = "Dummy sentence"
        self.MAX_SEQ_LENGTH: int = 128
        self.device: str = "cpu"

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
        return list_sentences

    def _extract_main_label(self, label: str) -> str:
        """
        Extract the main label from the given NER label

        Args:
            label (str): The NER label to extract the main label from.

        Returns:
            str: The main label extracted from the NER label
        """
        if label != "O":
            label = label.split("-")[1]
        return label

    def _join_word_labels_no_pos(
        self,
        word_labels: List[Tuple[List[int], str, Union[int, float], int]],
    ) -> List[Tuple[str, str, Union[float, int]]]:
        """
        Join word labels without positional information to form full word labels
        Args:
            word_labels (List[Tuple[List[int], str, Union[int, float], int]]): The word labels
                to join
        Returns:
        List[Tuple[str, str, Union[float, int]]]: The joiend full word labels
        """
        full_word_labels = []
        combined_word = []
        combined_word_id = []

        for i in range(len(word_labels)):
            (word, label, sco, word_id) = word_labels[i]
            label = self._extract_main_label(label)

            combined_word += word
            combined_word_id += [word_id]
            # last element
            if i == len(word_labels) - 1:
                if label != "O":
                    full_word_labels += [
                        (
                            self.compiled_ner_pipeline.tokenizer.decode(combined_word),
                            label,
                            sco,
                        )
                    ]
                break

            (_, label_next, sco_next, word_id_next) = word_labels[i + 1]
            label_next = self._extract_main_label(label_next)
            # flush out connected word tokens
            if (label != label_next) or (word_id != word_id_next - 1):
                if label != "O":
                    full_word_labels += [
                        (
                            self.compiled_ner_pipeline.tokenizer.decode(combined_word),
                            label,
                            sco,
                        )
                    ]
                combined_word = []
        return full_word_labels

    def _join_word_labels(
        self, word_labels: List[Tuple[List[int], str, Union[int, float], int, Any]]
    ) -> List[Tuple[str, str, Union[float, int], int, int]]:
        """
        Join word labels with positional information to form full word labels
        Args:
            word_labels (List[Tuple[List[int], str, Union[int, float], int, Any]]): The word
                labels to join
        Returns:
            List[Tuple[str, str, Union[float, int], int, int]]: Joined full word labels
        """
        full_word_labels = []
        combined_word = []
        combined_word_id = []
        combined_span = []

        for i in range(len(word_labels)):
            (word, label, sco, word_id, span) = word_labels[i]
            label = self._extract_main_label(label)

            combined_word += word
            combined_word_id += [word_id]  # unecessary?
            combined_span += span
            # last element
            if i == len(word_labels) - 1:
                if label != "O":

                    x = self.compiled_ner_pipeline.tokenizer.decode(combined_word)

                    start_pos = int(combined_span[0])
                    end_pos = start_pos + len(x)

                    full_word_labels += [(x, label, sco, start_pos, end_pos)]
                break

            (_, label_next, sco_next, word_id_next, span) = word_labels[i + 1]
            label_next = self._extract_main_label(label_next)
            # flush out connected word tokens
            if (label != label_next) or (word_id != word_id_next - 1):
                if label != "O":

                    x = self.compiled_ner_pipeline.tokenizer.decode(combined_word)

                    start_pos = int(combined_span[0])
                    end_pos = start_pos + len(x)

                    full_word_labels += [(x, label, sco, start_pos, end_pos)]
                combined_word = []
                combined_span = []
        return full_word_labels

    def filter_word_preds(
        self,
        word_preds: Any,
    ) -> Union[
        List[Tuple[List[int], str, Union[int, float], int, Any]],
        List[Tuple[List[int], str, Union[int, float], int]],
    ]:
        """
        Filter out word predictions based on the label to remove 'O' labels
        Args:
            word_preds (Any): The word predictions to filter
        Returns:
            Union[
                List[Tuple[List[int], str, Union[int, float], int, Any]],
                List[Tuple[List[int], str, Union[int, float], int]],
            ]: Filtered word predictions

        NOTE: word_preds mypy seems to reject typing:
        Union[
            List[Tuple[List[int], str, Union[int, float], int, Any]],
            List[Tuple[List[int], str, Union[int, float], int]],
        ]

        """
        output = []
        for info in word_preds:
            # second index holds label
            if info[1] != "O":
                output += [info]
        return output

    def inference_batch(
        self, sentences: List[str], sample_index: int, return_pos: bool
    ) -> Union[
        List[List[Tuple[str, str, Union[int, float], int, int]]],
        List[List[Tuple[str, str, Union[int, float]]]],
    ]:
        """
        Performs inference on a batch of sentences to extract NER labels

        Args:
            sentences (List[str]): The list of sentencess to perform inference on
            sample_index (int): Index of the sentences
            return_pos (bool): Flag indicating whether to return positional information in the
                output

        Returns:
            ) -> Union[
                List[List[Tuple[str, str, Union[int, float], int, int]]],
                List[List[Tuple[str, str, Union[int, float]]]],
            ]: Inferred NER labels for each sentence in the batch
        """
        ner_batch_labels = []
        if return_pos:
            self.inputs = self.compiled_ner_pipeline.tokenizer(
                sentences,
                padding="max_length",
                max_length=self.MAX_SEQ_LENGTH,
                truncation=True,
                return_tensors="pt",
                return_offsets_mapping=True,
            )
            offset_mappings = self.inputs["offset_mapping"]
        else:
            self.inputs = self.compiled_ner_pipeline.tokenizer(
                sentences,
                padding="max_length",
                max_length=self.MAX_SEQ_LENGTH,
                truncation=True,
                return_tensors="pt",
            )

        ids = self.inputs["input_ids"].to(self.device)
        mask = self.inputs["attention_mask"].to(self.device)
        neuron_inputs = ids, mask

        outputs = self.compiled_ner_pipeline.model.forward(*neuron_inputs)[0]
        out = torch.nn.functional.softmax(
            outputs, dim=2
        )  # transfer output to probability
        predictions = torch.argmax(outputs, dim=2)  # get the max index,6*128

        prob = torch.max(out, dim=2).values

        for sentence_index in range(len(sentences)):

            tokens = self.inputs.tokens(sentence_index)
            wordpiece_preds = [
                (token, self.id2label[prediction], pro)
                for token, prediction, pro in zip(
                    tokens,
                    predictions[sentence_index].detach().numpy(),
                    prob[sentence_index].detach().numpy(),
                )
            ]
            word_preds: Union[
                List[Tuple[List[int], str, Union[int, float], int, Any]],
                List[Tuple[List[int], str, Union[int, float], int]],
            ] = []  # type: ignore

            word_ids = self.inputs.word_ids(batch_index=sentence_index)
            word_id_prev = -1
            i = 0

            while i < len(word_ids):
                word_id = word_ids[i]
                token = tokens[i]

                if token == "[SEP]":
                    break

                if word_id is not None:
                    if word_id != word_id_prev:
                        word_range = self.inputs.word_to_tokens(
                            batch_or_word_index=sentence_index, word_index=word_id
                        )
                        token_id_list = ids[sentence_index][
                            word_range[0] : word_range[1]  # noqa: E203
                        ].tolist()
                        if return_pos:
                            word_preds.extend(
                                [
                                    (  # type: ignore
                                        token_id_list,
                                        wordpiece_preds[i][1],
                                        wordpiece_preds[i][2],
                                        word_id,
                                        offset_mappings[sentence_index][i],
                                    )
                                ]
                            )

                        else:
                            word_preds.extend(
                                [
                                    (  # type: ignore
                                        token_id_list,
                                        wordpiece_preds[i][1],
                                        wordpiece_preds[i][2],
                                        word_id,
                                    )
                                ]
                            )

                word_id_prev = word_id
                i += 1

            word_preds = self.filter_word_preds(word_preds)
            # get sentence index
            sen_index = sample_index * self.MAX_BATCH_SIZE + sentence_index
            ent: str
            catg: str
            sco: Union[int, float]
            start_pos: int
            end_pos: int
            if return_pos:
                full_word_preds = self._join_word_labels(word_preds)  # type: ignore
                full_word_preds = [
                    (ent, catg, sco, sen_index, start_pos, end_pos)  # type: ignore
                    for ent, catg, sco, start_pos, end_pos in full_word_preds
                ]
            else:
                full_word_preds = self._join_word_labels_no_pos(word_preds)  # type: ignore
                full_word_preds = [  # type: ignore
                    (ent, catg, sco, sen_index)  # type: ignore
                    for ent, catg, sco in full_word_preds
                ]

            ner_batch_labels += [full_word_preds]
        return ner_batch_labels

    def inference(
        self, sentences: List[str], return_pos: bool
    ) -> List[Tuple[str, str, Union[int, float], int, int, int]]:
        """
        Perform inference on a list of sentences to extract NER labels
        Args:
            sentences (List[str]): The list of sentences to perform inference on
            return_pos (bool): Flag indicating whether ot return positional information
                in the output

        Returns:
            List[Tuple[str, str, Union[int, float], int, int, int]]: The inferred NER labels
        """

        def flatten(list: Any) -> Generator:
            for el in list:
                if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
                    yield from flatten(el)
                else:
                    yield el

        loader = DataLoader(sentences, batch_size=self.MAX_BATCH_SIZE, shuffle=False)
        ner_labels: List[Any] = []

        sample_index = 0  # to record sentence index
        for sample in loader:
            len_sample = len(sample)

            if len_sample < self.MAX_BATCH_SIZE:
                sample += [self.DUMMY_SENTENCE] * (self.MAX_BATCH_SIZE - len_sample)

            ner_batch_labels = self.inference_batch(sample, sample_index, return_pos)

            ner_batch_labels = ner_batch_labels[:len_sample]
            for n in ner_batch_labels:
                ner_labels += n

            sample_index += 1
        return ner_labels

    def postprocess(
        self, ner_labels: Any, return_pos: bool
    ) -> List[Dict[str, Union[float, int, str]]]:
        """
        Postprocess NER labels to dictionary format
        Args:
            ner-Labels (Any): NER labels to postprocess
            return_pos (bool): Flag indicating whether the input NER labels contain positional
                information
        """
        ner_labels = set(ner_labels)
        sorted_entities = []
        entities = []
        if return_pos:
            for word, label, sco, coun, start_pos, end_pos in ner_labels:
                entities += [
                    {
                        "entity_type": label,
                        "entity_text": word,
                        "score": str(sco),
                        "sentence_index": coun,
                        "start": start_pos,
                        "end": end_pos,
                    }
                ]
            sorted_entities = sorted(
                entities, key=lambda e: (e["sentence_index"], e["start"])
            )
        else:
            for word, label, sco, coun in ner_labels:
                entities += [
                    {
                        "entity_type": label,
                        "entity_text": word,
                        "score": str(sco),
                        "sentence_index": coun,
                    }
                ]
            sorted_entities = sorted(entities, key=lambda e: e["sentence_index"])

        return sorted_entities

    def extract_entities(
        self, sentences: str, return_pos: bool
    ) -> List[Dict[str, Union[float, int, str]]]:
        """
        Extract named entities from input sentence using NER
        Args:
            sentences (str): The input sentences to extract entities from
            return_pos (bool): Flag indiciating whether to return positional information in the
                output
        Returns:
            List[Dict[str, Union[float, int, str]]]: Extracted named entities in dictionary
                format
        """
        list_sentences = self.preprocess(sentences)
        ner_labels = self.inference(list_sentences, return_pos)
        entities = self.postprocess(ner_labels, return_pos)
        return entities
