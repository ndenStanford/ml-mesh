"""Compiled sentiment."""

# Standard Library
import os
import string
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ML libs
import torch

# 3rd party libraries
# import numpy as np
import regex

# Internal libraries
from onclusiveml.compile import CompiledPipeline
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp import preprocess
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer


# from nptyping import NDArray

logger = get_default_logger(__name__, level=20)


class CompiledSentiment:
    """Class for performing sentiment analysis using neuron compiled Sent pipeline."""

    def __init__(
        self,
        compiled_sent_pipeline: CompiledPipeline,
    ):
        """Initalize the CompiledSentiment object.

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
        """Save compiled Sent pipeline to specified directory.

        Args:
            directory (Union[Path, str]): Directory to save the compiled Sent pipeline
        """
        self.compiled_sent_pipeline.save_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "CompiledSentiment":
        """Load compiledSent object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                sent pipeline
        Returns:
            CompiledSentiment: The loaded pre-trained CompiledSentiment object
        """
        compiled_sent_pipeline = CompiledPipeline.from_pretrained(
            os.path.join(directory, "compiled_sent_pipeline")
        )

        return cls(
            compiled_sent_pipeline=compiled_sent_pipeline,
        )

    def preprocess(self, sentences: str, language: str) -> str:
        """Preprocess the input sentences by removing unwanted content inside text and tokenizing.

        Args:
            sentences (str): Input sentences
            language (str): Language of input sentences
        Return:
            str: Tokenized sentences
        """
        sentences = preprocess.remove_html(sentences)
        sentences = preprocess.remove_whitespace(sentences)
        tokenizer = SentenceTokenizer()
        list_sentences = tokenizer.tokenize(content=sentences, language=language)[
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

        combined_text = " ".join(list_sentences)
        return combined_text

    # def inference(self, list_sentences: NDArray) -> NDArray:
    #     """Compute sentiment probability of each sentence.
    #     Args:
    #         list_sentences (NDArray): Input list of sentences
    #     Returns:
    #         sentiment_probs (NDArray): List of sentiment probability
    #     """
    #     self.inputs = self.compiled_sent_pipeline.tokenizer(
    #         list_sentences,
    #         return_tensors="pt",
    #     )
    #     res = self.compiled_sent_pipeline.model(**self.inputs)
    #     sentiment_probs_arr: NDArray = (
    #         res["logits"].clone().detach().numpy().astype(float)
    #     )
    #     # assert sentiment_probs_arr.shape[0] == n_sentence
    #     assert sentiment_probs_arr.shape[0] == len(list_sentences)
    #     return sentiment_probs_arr
    # def postprocess(
    #     self,
    #     sentiment_probs: NDArray,
    #     list_sentences: List[str],
    #     entities: Optional[List[Dict[str, Union[str, List]]]],
    # ) -> Dict[str, Union[float, str, List]]:
    #     """Compute sentiment probability of each sentence.
    #     Args:
    #         sentiment_probs (NDArray): List of sentiment probability
    #         list_sentences (List[str]): Input list of sentences
    #         entities (Optional[List[Dict[str, Union[str, List]]]]):
    #             List of detected entities from the NER model
    #     Returns:
    #         sentiment_result (Dict[str, Union[float, str, List]]): List of sentiment probability
    #     """
    #     logits = np.exp(sentiment_probs.reshape(-1, self.NUM_LABELS))
    #     sentiment_probs = np.around(logits / np.sum(logits, axis=1).reshape(-1, 1), 4)
    #     agg_sentiment_probs = np.around(np.mean(sentiment_probs, axis=0), 4)
    #     sentiment_result: Dict[str, Union[float, str, List[Any]]] = {}
    #     sentiment_result["label"] = self._decide_label(
    #         agg_sentiment_probs[2], agg_sentiment_probs[1], agg_sentiment_probs[0]
    #     )
    #     sentiment_result["sentence_pos_probs"] = sentiment_probs[:, 2].tolist()
    #     sentiment_result["sentence_neg_probs"] = sentiment_probs[:, 0].tolist()
    #     sentiment_result["negative_prob"] = agg_sentiment_probs[0]
    #     sentiment_result["positive_prob"] = agg_sentiment_probs[2]
    #     if entities is not None:
    #         entity_sentiment: List[Dict[str, Union[str, List[Any]]]] = (
    #             self._add_entity_sentiment(list_sentences, sentiment_result, entities)
    #         )
    #         sentiment_result["entities"] = entity_sentiment
    #     return sentiment_result
    # def _decide_label(self, pos: float, neu: float, neg: float) -> str:
    #     """Helper function to decide final sentiment.
    #     The threshold has been calibrated to align with the customer expectation
    #     Args:
    #         pos (float): Probability of positive sentiment
    #         neu (float): Probability of neutral sentiment
    #         neg (float): Probability of negative sentiment
    #     Returns:
    #         val (str): Final sentiment label
    #     """
    #     neg = neg - 0.2 * pos
    #     pos = pos * 1.7
    #     if pos > 1 or neg < 0:
    #         pos = 1
    #         neg = 0
    #     neu = 1 - pos - neg
    #     val = (
    #         "positive"
    #         if (pos > neg) and (pos > neu)
    #         else (
    #             "neutral"
    #             if (neu > neg) and (neu > pos)
    #             else "negative" if (neg > pos) and (neg > neu) else "neutral"
    #         )
    #     )
    #     return val
    # def _add_entity_sentiment(
    #     self,
    #     sentences: List[Any],
    #     res: Dict,
    #     entities: List[Dict[str, Union[str, List]]],
    # ) -> List[Dict[str, Union[str, List]]]:
    #     """Augment the entity with the corresponding sentiment.
    #     Args:
    #         sentences (List[Any]): List of sentences from the article
    #         res (Dict): List of sentiment probability corresponding to sentences
    #         entities (List[Dict[str, Union[str, List]]]):
    #             List of detected entities from the NER model
    #     Returns:
    #         entity_sentiment (List[Dict[str, Union[str, List]]]):
    #             List of detected entities with sentiment attached to them
    #     """
    #     sentence_pos_probs = res["sentence_pos_probs"]
    #     sentence_neg_probs = res["sentence_neg_probs"]
    #     sentence_neu_probs = [
    #         1 - pos - neg for pos, neg in zip(sentence_pos_probs, sentence_neg_probs)
    #     ]
    #     entity_sentiment = []
    #     for entity in entities:
    #         try:
    #             entity_text = entity.get("entity_text")
    #             indexes = entity.get("sentence_indexes", None)
    #             if indexes is None:
    #                 indexes = [
    #                     i
    #                     for i, sentence in enumerate(sentences)
    #                     if (sentence.find(entity_text) != -1)
    #                 ]
    #             i = 0
    #             pos: float = 0
    #             neg: float = 0
    #             neu: float = 0
    #             for index in indexes:
    #                 pos += sentence_pos_probs[index]
    #                 neg += sentence_neg_probs[index]
    #                 neu += sentence_neu_probs[index]  # type: ignore
    #                 i += 1
    #             if i == 0:
    #                 entity["sentiment"] = "neutral"
    #             else:
    #                 pos = pos / i
    #                 neg = neg / i
    #                 neu = neu / i
    #                 entity["sentiment"] = self._decide_label(pos, neu, neg)
    #             entity_sentiment.append(entity)
    #         except Exception as e:
    #             logger.error(e)
    #             entity["sentiment"] = "neutral"
    #             entity_sentiment.append(entity)
    #     return entity_sentiment

    def chunk_text_and_predict_proba_absa(
        self,
        input_ids: List,
        attention_mask: List,
        aspect_input_ids: List,
        aspect_attention_mask: List,
        total_len: int,
        global_sentiment_tag: bool = "False",
        window_length: int = 500,
    ) -> List:
        """Splits input text into chunks then applies model to each chunk and computes probabilities.

        Args:
            input_ids (List[int]): List of token ids representing the input text.
            attention_mask (List[int]): List of attention masks corresponding to input_ids.
            total_len (int): Total length of the input_ids.
            model_type (str): is a bert/distilbert/roberta model? different input_ids for cls and sep

        Returns:
            proba_list (List[torch.Tensor]): List of probability tensors for each chunk.
        """
        proba_list = []
        # Calculate the number of chunks needed
        num_chunks = total_len // window_length + 1
        chunk_size = (total_len + num_chunks) // num_chunks

        start = 0
        loop = True

        cls_id, sep_id = [1], [2]

        while loop:
            end = min(start + chunk_size, total_len)
            # If the end index exceeds total length, set the flag to False and adjust the end index
            if end >= total_len:
                loop = False
                end = total_len
            # 1 => Define the text chunk
            input_ids_chunk = input_ids[start:end]
            attention_mask_chunk = attention_mask[start:end]
            # 2 => Append [CLS] and [SEP] & aspect tokens
            if global_sentiment_tag:
                input_ids_chunk = (
                    cls_id
                    + cls_id
                    + aspect_input_ids
                    + input_ids_chunk
                    + sep_id
                    + aspect_input_ids
                    + sep_id
                    + sep_id
                )
                attention_mask_chunk = (
                    [1]
                    + [1]
                    + aspect_attention_mask
                    + attention_mask_chunk
                    + [1]
                    + aspect_attention_mask
                    + [1]
                    + [1]
                )
            else:
                input_ids_chunk = (
                    cls_id
                    + cls_id
                    + input_ids_chunk
                    + sep_id
                    + aspect_input_ids
                    + sep_id
                )
                attention_mask_chunk = (
                    [1] + [1] + attention_mask_chunk + [1] + aspect_attention_mask + [1]
                )
            # 3 Convert regular python list to Pytorch Tensor
            input_dict = {
                "input_ids": torch.Tensor([input_ids_chunk]).long(),
                "attention_mask": torch.Tensor([attention_mask_chunk]).int(),
            }

            with torch.no_grad():
                outputs = self.compiled_sent_pipeline.model(**input_dict)

                probabilities = torch.nn.functional.softmax(outputs[0], dim=1)
            # print('Probability :',probabilities)
            start = end
            proba_list.append(probabilities)
        # print('Proba list :',proba_list)
        return proba_list

    def get_tag_from_proba_absa(self, proba_list: List) -> tuple[str, list]:
        """From probability to sentiment tag.

        Args:
        proba_list: probability list

        Output:
        Tuple: sentiment tag -> str, probability_list -> list
        """
        # Ensures that gradients are not computed, saving memory
        with torch.no_grad():
            # Stack the list of tensors into a single tensor
            stacks = torch.stack(proba_list)
            # print('STACKS :',stacks)
            # Resize the tensor to match the dimensions needed for mean computation
            # don't need it if batch inference
            # stacks = stacks.resize(stacks.shape[0], stacks.shape[2])
            # print(stacks)
            # Compute the mean along the zeroth dimension (i.e., the chunk dimension)
            mean = stacks.mean(dim=0)
            # get number tag
            num_tag = torch.argmax(mean).item()
            if num_tag == 2:
                tag = "positive"
            elif num_tag == 1:
                tag = "neutral"
            else:
                tag = "negtive"
            return tag, mean

    # compile inference chunk function
    def chunk_tag_predict_absa(
        self,
        text: str,
        entities: List[Dict[str, Union[str, List]]],
        window_length: int = 500,
    ) -> dict:
        """Get final sentiment output.

        Args:
        text: str, input article
        entities: List, target entities
        window_length: int

        Outputs:
        sentiment
        """
        tokens = self.compiled_sent_pipeline.tokenizer(text, add_special_tokens=False)
        # global sentiment
        global_aspect_tokens = self.compiled_sent_pipeline.tokenizer(
            "Global Sentiment", add_special_tokens=False
        )
        global_proba_list = self.chunk_text_and_predict_proba_absa(
            tokens["input_ids"],
            tokens["attention_mask"],
            global_aspect_tokens["input_ids"],
            global_aspect_tokens["attention_mask"],
            len(tokens["input_ids"]),
            global_sentiment_tag=True,
            window_length=window_length,
        )
        global_tag, global_prob = self.get_tag_from_proba_absa(global_proba_list)
        # tag for global sentiment or not
        entity_sentiment = []
        for entity in entities:
            try:
                entity_text = entity.get("entity_text")
                global_sentiment_tag = False
                entity_tokens = self.compiled_sent_pipeline.tokenizer(
                    entity_text, add_special_tokens=False
                )
                entity_proba_list = self.chunk_text_and_predict_proba_absa(
                    tokens["input_ids"],
                    tokens["attention_mask"],
                    entity_tokens["input_ids"],
                    entity_tokens["attention_mask"],
                    len(tokens["input_ids"]),
                    global_sentiment_tag,
                    window_length=window_length,
                )
                entity_tag, entity_prob = self.get_tag_from_proba_absa(
                    entity_proba_list
                )
                entity["sentiment"] = entity_tag
                entity_sentiment.append(entity)
            except Exception as e:
                logger.error(e)
                entity["sentiment"] = "neutral"
                entity_sentiment.append(entity)
        # generate final output
        sentiment_result: Dict[str, Union[float, str, List[Any]]] = {}
        sentiment_result["label"] = global_tag
        sentiment_result["negative_prob"] = global_prob[0]
        sentiment_result["positive_prob"] = global_prob[2]

        if entities is not None:
            sentiment_result["entities"] = entity_sentiment

        return sentiment_result

    def __call__(
        self,
        sentences: str,
        entities: Optional[List[Dict[str, Union[str, List]]]] = None,
        language: str = "en",
    ) -> Dict[str, Union[float, str, List]]:
        """Sentiment detection of each entity input sentence.

        Args:
            sentences (str): The input sentences to extract entities from
            entities (Optional[List[Dict[str, Union[str, List]]]]):
                List of detected entities from the NER model
            language (str): Language of input sentences
        Returns:
            sentiment_output (Dict[str, Union[float, str, List]]):
                Extracted named entities in dictionary format
        """
        preprocessed_sentences = self.preprocess(sentences, language)
        sentiment_output = self.chunk_tag_predict_absa(
            self, preprocessed_sentences, entities, window_length=500
        )
        return sentiment_output
