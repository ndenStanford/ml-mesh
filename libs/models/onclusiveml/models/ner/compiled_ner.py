# Standard Library
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

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
            0: "O",  # 'O' label indicates no named entity
            1: "B-MISC",  # 'B-' prefix indicates the beginning of a named entity
            2: "I-MISC",  # 'I-' prefix indicates a continuation of a named entity
            3: "B-PER",
            4: "I-PER",
            5: "B-ORG",
            6: "I-ORG",
            7: "B-LOC",
            8: "I-LOC",
        }
        # Initialise sentence tokenizer
        self.sentence_tokenizer = SentenceTokenizer()

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
            word_labels (List[Tuple[List[int], str, Union[int, float], int]]):
                The word labels to join, each tuple contains:
                - List of token IDs representing a word
                - A string representing the NER label of the word
                - A float or int representing the score of NER label
                - An int representing the word's ID within the sentence
        Returns:
            List[Tuple[str, str, Union[float, int]]]: The joiend full word labels
                Each tuple contains:
                - A string representing the full word
                - A string representing the NER label of the word
                - A float or int representing the score of the NER label
        """
        full_word_labels = []  # List to store the joined full word labels
        combined_word = []  # List to combine the tokenIDs of a word for decoding

        for i in range(len(word_labels)):
            (word, label, sco, word_id) = word_labels[i]

            # Extract main NER label (removing 'B-' and 'I-' prefixes)
            label = self._extract_main_label(label)

            # Combine token IDs of the word into a single list
            combined_word += word

            # Check if we have reached the last word in the sentence
            if i == len(word_labels) - 1:
                if label != "O":
                    # Decode the combined word token IDs to get full word string
                    # And add the full word label to the list
                    full_word_labels += [
                        (
                            self.compiled_ner_pipeline.tokenizer.decode(combined_word),
                            label,
                            sco,
                        )
                    ]
                break

            # Check the NER label of the next word and the word's ID to determine
            # if it's a seperate entity
            (_, label_next, sco_next, word_id_next) = word_labels[i + 1]
            label_next = self._extract_main_label(label_next)

            # If the label changes or the word IDs are not consecutive, it's a seperate entity
            # Flush out the combined_word and add the full word label to the full_word_labels list
            if (label != label_next) or (word_id != word_id_next - 1):
                if label != "O":
                    # Decode the combined word token IDs to get full word string
                    # And add the full word label to the list
                    full_word_labels += [
                        (
                            self.compiled_ner_pipeline.tokenizer.decode(combined_word),
                            label,
                            sco,
                        )
                    ]
                combined_word = []  # reset for the next entity
        return full_word_labels

    def _join_word_labels(
        self, word_labels: List[Tuple[List[int], str, Union[int, float], int, Any]]
    ) -> List[Tuple[str, str, Union[float, int], int, int]]:
        """
        Join word labels with positional information to form full word labels
        Args:
            word_labels (List[Tuple[List[int], str, Union[int, float], int, Any]]): The word
                labels to join2, each tuple contains:
                - A list of token IDs representing a word
                - A string representing the NER label of the word
                - A float or int representing the score of the NER label
                - An int representing the word's ID within the sentence
                - An additional 'span' value used for positional information
        Returns:
            List[Tuple[str, str, Union[float, int], int, int]]: Joined full word labels
                each tuple contains:
                - A string representing the full word
                - A string representing the NER label of the word
                - A float or int representing the score of the NER label
                - An int representing sentence index
                - An int representing the start position of the word
                - An int representing the end position of the word
        """
        full_word_labels = []  # List to store the joined full word labels
        combined_word = []  # List to combined the token IDs of a word for decoding
        combined_span = []  # List to combine the span alues for positional info

        for i in range(len(word_labels)):
            (word, label, sco, word_id, span) = word_labels[i]
            # Extract the main NER label (removing 'B-' and 'I'' prefixes)
            label = self._extract_main_label(label)
            combined_word += word  # Combine token IDs of the word into a single list
            combined_span += span  # Combine the span values for positional information

            # Check if we have reached the last word in the sentence
            if i == len(word_labels) - 1:
                if label != "O":
                    # Decode the combined word token IDs to get the full word string
                    x = self.compiled_ner_pipeline.tokenizer.decode(combined_word)

                    # Calculate the start position of the word in the sentence
                    start_pos = int(combined_span[0])
                    # Calculate the end position of teh word in the sentence
                    end_pos = start_pos + len(x)
                    # Add the full word label to the list along with positional information
                    full_word_labels += [(x, label, sco, start_pos, end_pos)]
                break

            # Check the NER label of the next word, the word's ID, and the span to determine
            # if it's a seperate entity
            (_, label_next, sco_next, word_id_next, span) = word_labels[i + 1]
            label_next = self._extract_main_label(label_next)

            # If the label changes or the word IDs are not consecutive, it's a seperate entity
            # Flush out the combined_word and combined_span and add the full word label to the list
            if (label != label_next) or (word_id != word_id_next - 1):
                if label != "O":
                    # Decode the combined word token IDs to get the full word string
                    x = self.compiled_ner_pipeline.tokenizer.decode(combined_word)

                    # Calculate the start position of the word in the sentence
                    start_pos = int(combined_span[0])

                    # Calculate the end position of the word in the sentence
                    end_pos = start_pos + len(x)

                    # Add the full word label to the list along with positional information
                    full_word_labels += [(x, label, sco, start_pos, end_pos)]
                combined_word = []  # Reset combined_word for the next entity
                combined_span = []  # Reset combined_span for the next entity
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
                Each element contains:
                - A list of token IDs representing a word
                - A string representing the NER label of the word
                - A float or int representing the score of the NER label
                - An int representing the word's ID within the sentence
                - An additional 'span' value used for positional information
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
        output = []  # List to store filtered word predictions
        for info in word_preds:
            # second index holds NER label
            # 'O' label indicates no named entity, so we filter it out
            if info[1] != "O":
                # Add the word prediction to the output list if the label is not 'O'
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
        # List to store the inferred NER labels for each sentence in the batch
        ner_batch_labels = []
        if return_pos:
            # Tokenise the sentences using the NER pipeline's tokenizer and get the offset mappings
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
            # Tokenise the sentences using the NER pipeline's tokenizer without offset mappings
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

        # Perform forward pass on the NER model to get the outputs
        outputs = self.compiled_ner_pipeline.model.forward(*neuron_inputs)[0]

        # transfer output to probabilities
        out = torch.nn.functional.softmax(outputs, dim=2)
        # Get the index of the highest probability (NER label)
        predictions = torch.argmax(outputs, dim=2)

        prob = torch.max(out, dim=2).values

        # Loop through each sentence in the batch to retrieve all full NER labels
        for sentence_index in range(len(sentences)):
            # Get the tokens of the current sentence
            tokens = self.inputs.tokens(sentence_index)

            # List to store word-level predictions for each token in the sentence
            wordpiece_preds = [
                (token, self.id2label[prediction], pro)
                for token, prediction, pro in zip(
                    tokens,
                    predictions[sentence_index].detach().numpy(),
                    prob[sentence_index].detach().numpy(),
                )
            ]
            # List to store the word-level predictions for the sentence
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
                    # Check if the word ID has chaged, indicating a new word entity
                    if word_id != word_id_prev:
                        word_range = self.inputs.word_to_tokens(
                            batch_or_word_index=sentence_index, word_index=word_id
                        )
                        token_id_list = ids[sentence_index][
                            word_range[0] : word_range[1]  # noqa: E203
                        ].tolist()
                        # Append the word-level prediction
                        # (token IDs label, score, word ID, and offset span)
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
                            # Append the word-level prediction (token IDs label, score, word ID)
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

            # Filter out 'O' labels from word_preds to get only named entites
            word_preds = self.filter_word_preds(word_preds)

            # Get the sentence index for the current sentence in the batch
            sen_index = sample_index * self.MAX_BATCH_SIZE + sentence_index
            ent: str
            catg: str
            sco: Union[int, float]
            start_pos: int
            end_pos: int
            if return_pos:
                # Join the word labels with pos information to form full word labels
                full_word_preds = self._join_word_labels(word_preds)  # type: ignore

                # Add sentence index and positional information to the full word labels
                full_word_preds = [
                    (ent, catg, sco, sen_index, start_pos, end_pos)  # type: ignore
                    for ent, catg, sco, start_pos, end_pos in full_word_preds
                ]
            else:
                # Join word labels without positional information to form full word labels
                full_word_preds = self._join_word_labels_no_pos(word_preds)  # type: ignore

                # Add sentence index to the full word labels
                full_word_preds = [  # type: ignore
                    (ent, catg, sco, sen_index)  # type: ignore
                    for ent, catg, sco in full_word_preds
                ]

            # Add the full word labels to ner_batch_labels
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
        self, sentences: str, language: str, return_pos: bool
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
        list_sentences = self.preprocess(sentences, language)
        ner_labels = self.inference(list_sentences, return_pos)
        entities = self.postprocess(ner_labels, return_pos)
        return entities
