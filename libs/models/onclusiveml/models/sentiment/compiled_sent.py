# Standard Library
import os
import re
import string
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ML libs
import torch

# 3rd party libraries
import numpy as np
import regex
from bs4 import BeautifulSoup
from nptyping import NDArray

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer


logger = get_default_logger(__name__, level=20)


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
        self.MAX_SEQ_LENGTH = (
            compiled_sent_pipeline.compiled_pipeline.model.compilation_specs[
                "tracing__max_length"
            ]
        )
        self.MAX_BATCH_SIZE = (
            compiled_sent_pipeline.compiled_pipeline.model.compilation_specs[
                "tracing__batch_size"
            ]
        )
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

    def inference(self, list_sentences: NDArray) -> NDArray:
        """
        Compute sentiment probability of each sentence
        Args:
            list_sentences (NDArray): Input list of sentences
        Returns:
            sentiment_probs (NDArray): List of sentiment probability
        """
        self.inputs = self.compiled_sent_pipeline.tokenizer(
            list_sentences,
            padding="max_length",
            max_length=self.MAX_SEQ_LENGTH,
            truncation=True,
            return_tensors="pt",
        )

        input_ids = self.inputs["input_ids"].to(self.device)
        attention_masks = self.inputs["attention_mask"].to(self.device)

        sentiment_probs = []
        n_sentence = len(input_ids)

        while len(input_ids) > 0:
            it_input_ids = input_ids[: self.MAX_BATCH_SIZE].clone().detach()
            it_attention_masks = attention_masks[: self.MAX_BATCH_SIZE].clone().detach()

            diff_size = self.MAX_BATCH_SIZE - it_input_ids.size()[0]

            if diff_size > 0:
                it_input_ids = torch.cat(
                    (
                        it_input_ids,
                        torch.tensor(np.zeros([diff_size, 128]), dtype=torch.int64),
                    ),
                    0,
                )
                it_attention_masks = torch.cat(
                    (
                        it_attention_masks,
                        torch.tensor(np.zeros([diff_size, 128]), dtype=torch.int64),
                    ),
                    0,
                )
            res = self.compiled_sent_pipeline.model(
                *(it_input_ids, it_attention_masks), return_dict=False
            )  # [0]

            if diff_size > 0:
                res = res[: (self.MAX_BATCH_SIZE - diff_size)]

            try:
                sentiment_probs += res.tolist()
            except Exception as e:
                raise e

            input_ids = input_ids[self.MAX_BATCH_SIZE :]
            attention_masks = attention_masks[self.MAX_BATCH_SIZE :]

        sentiment_probs_arr: NDArray = np.array(sentiment_probs)

        assert sentiment_probs_arr.shape[0] == n_sentence
        return sentiment_probs_arr

    def postprocess(
        self,
        sentiment_probs: NDArray,
        list_sentences: List[str],
        entities: Optional[List[Dict[str, Union[str, List]]]],
    ) -> Dict[str, Union[float, str, List]]:
        """
        Compute sentiment probability of each sentence
        Args:
            sentiment_probs (NDArray): List of sentiment probability
            list_sentences (List[str]): Input list of sentences
            entities (Optional[List[Dict[str, Union[str, List]]]]):
                List of detected entities from the NER model
        Returns:
            sentiment_result (Dict[str, Union[float, str, List]]): List of sentiment probability
        """
        logits = np.exp(sentiment_probs.reshape(-1, self.NUM_LABELS))

        sentiment_probs = np.around(logits / np.sum(logits, axis=1).reshape(-1, 1), 4)

        agg_sentiment_probs = np.around(np.mean(sentiment_probs, axis=0), 4)

        sentiment_result: Dict[str, Union[float, str, List[Any]]] = {}
        sentiment_result["label"] = self._decide_label(
            agg_sentiment_probs[2], agg_sentiment_probs[1], agg_sentiment_probs[0]
        )
        sentiment_result["sentence_pos_probs"] = sentiment_probs[:, 2].tolist()
        sentiment_result["sentence_neg_probs"] = sentiment_probs[:, 0].tolist()
        sentiment_result["negative_prob"] = agg_sentiment_probs[0]
        sentiment_result["positive_prob"] = agg_sentiment_probs[2]

        if entities is not None:
            entity_sentiment: List[
                Dict[str, Union[str, List[Any]]]
            ] = self._add_entity_sentiment(list_sentences, sentiment_result, entities)
            sentiment_result["entities"] = entity_sentiment

        return sentiment_result

    def _decide_label(self, pos: float, neu: float, neg: float) -> str:
        """
        Helper function to decide final sentiment.
        The threshold has been calibrated to align with the customer expectation
        Args:
            pos (float): Probability of positive sentiment
            neu (float): Probability of neutral sentiment
            neg (float): Probability of negative sentiment
        Returns:
            val (str): Final sentiment label
        """
        neg = neg - 0.2 * pos
        pos = pos * 1.7
        if pos > 1 or neg < 0:
            pos = 1
            neg = 0
        neu = 1 - pos - neg
        val = (
            "positive"
            if (pos > neg) and (pos > neu)
            else "neutral"
            if (neu > neg) and (neu > pos)
            else "negative"
            if (neg > pos) and (neg > neu)
            else "neutral"
        )
        return val

    def _add_entity_sentiment(
        self,
        sentences: List[Any],
        res: Dict,
        entities: List[Dict[str, Union[str, List]]],
    ) -> List[Dict[str, Union[str, List]]]:
        """
        Augment the entity with the corresponding sentiment
        Args:
            sentences (List[Any]): List of sentences from the article
            res (Dict): List of sentiment probability corresponding to sentences
            entities (List[Dict[str, Union[str, List]]]):
                List of detected entities from the NER model
        Returns:
            entity_sentiment (List[Dict[str, Union[str, List]]]):
                List of detected entities with sentiment attached to them
        """
        sentence_pos_probs = res["sentence_pos_probs"]
        sentence_neg_probs = res["sentence_neg_probs"]
        sentence_neu_probs = [
            1 - pos - neg for pos, neg in zip(sentence_pos_probs, sentence_neg_probs)
        ]

        entity_sentiment = []
        for entity in entities:
            try:
                entity_text = entity.get("text")
                indexes = entity.get("sentence_indexes", None)
                if indexes is None:
                    indexes = [
                        i
                        for i, sentence in enumerate(sentences)
                        if (sentence.find(entity_text) != -1)
                    ]

                i = 0
                pos: float = 0
                neg: float = 0
                neu: float = 0
                for index in indexes:
                    pos += sentence_pos_probs[index]
                    neg += sentence_neg_probs[index]
                    neu += sentence_neu_probs[index]  # type: ignore
                    i += 1

                if i == 0:
                    entity["sentiment"] = "neutral"
                else:
                    pos = pos / i
                    neg = neg / i
                    neu = neu / i
                    entity["sentiment"] = self._decide_label(pos, neu, neg)
                entity_sentiment.append(entity)
            except Exception as e:
                logger.error(e)
                entity["sentiment"] = "neutral"
                entity_sentiment.append(entity)

        return entity_sentiment

    def extract_sentiment(
        self,
        sentences: str,
        entities: Optional[List[Dict[str, Union[str, List]]]] = None,
    ) -> Dict[str, Union[float, str, List]]:
        """
        Sentiment detection of each entity input sentence
        Args:
            sentences (str): The input sentences to extract entities from
            entities (Optional[List[Dict[str, Union[str, List]]]]):
                List of detected entities from the NER model
        Returns:
            sentiment_output (Dict[str, Union[float, str, List]]):
                Extracted named entities in dictionary format
        """
        list_sentences = self.preprocess(sentences)
        sentiment_prob_list = self.inference(list_sentences)
        sentiment_output = self.postprocess(
            sentiment_prob_list, list_sentences, entities
        )
        return sentiment_output
