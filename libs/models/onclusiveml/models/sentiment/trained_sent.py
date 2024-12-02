"""Trained sentiment."""

# Standard Library
import string
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# ML libs
import torch
from transformers.pipelines import pipeline

# 3rd party libraries
import regex

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp import preprocess
from onclusiveml.nlp.tokenizers.sentence import SentenceTokenizer


logger = get_default_logger(__name__, level=20)


class TrainedSentiment:
    """Class for performing sentiment analysis using trained Sent pipeline."""

    def __init__(
        self,
        trained_sent_pipeline: pipeline,
    ):
        """Initalize the TrainedSentiment object.

        Args:
            trained_sent_pipeline (Pipeline): The trained Sent pipline used for inference
        """
        self.trained_sent_pipeline = trained_sent_pipeline
        self.unicode_strp = regex.compile(r"\p{P}")
        self.window_length: int = 500
        self.device: str = "cuda" if torch.cuda.is_available() else "cpu"

    @classmethod
    def from_pretrained(cls, directory: Union[Path, str]) -> "TrainedSentiment":
        """Load compiledSent object from specfied directory.

        Args:
            directory (Union[Path, str]): The directory path contained the pretrained compiled
                sent pipeline
        Returns:
            CompiledSentiment: The loaded pre-trained CompiledSentiment object
        """
        trained_sent_pipeline = pipeline(
            task="sentiment-analysis",
            model=directory,
            tokenizer=directory,
        )
        return cls(
            trained_sent_pipeline=trained_sent_pipeline,
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

    def chunk_text_and_predict_proba_absa(
        self,
        input_ids: List,
        attention_mask: List,
        aspect_input_ids: List,
        aspect_attention_mask: List,
        total_len: int,
        global_sentiment_tag: bool,
        window_length: int,
        device: str,
    ) -> List:
        """Splits input into chunks, combines with aspect tokens, and predicts sentiment probabilities for each chunk.

        Args:
            input_ids (List[int]): Token IDs representing the input text.
            attention_mask (List[int]): Attention mask corresponding to the input text tokens.
            aspect_input_ids (List[int]): Token IDs representing the aspect (e.g., entity or global context).
            aspect_attention_mask (List[int]): Attention mask corresponding to the aspect tokens.
            total_len (int): Total length of the input token IDs.
            global_sentiment_tag (bool):
                Whether the sentiment analysis is for global sentiment (True) or entity-specific sentiment (False).
            window_length (int): The maximum length of each chunk for processing.
            device (str): The device to perform inference on (e.g., "cpu" or "cuda").

        Returns:
            List[torch.Tensor]: A list of probability tensors, one for each chunk,
                where each tensor contains sentiment probabilities for negative, neutral, and positive classes.
        """
        # Ensure the model is on the correct device and in evaluation mode
        self.trained_sent_pipeline.model = self.trained_sent_pipeline.model.to(device)
        self.trained_sent_pipeline.model.eval()

        proba_list = []
        num_chunks = total_len // window_length + 1
        chunk_size = (total_len + num_chunks) // num_chunks

        start = 0
        loop = True

        cls_id = [self.trained_sent_pipeline.tokenizer.cls_token_id]
        sep_id = [self.trained_sent_pipeline.tokenizer.sep_token_id]

        while loop:
            end = min(start + chunk_size, total_len)
            if end >= total_len:
                loop = False
                end = total_len

            input_ids_chunk = input_ids[start:end]
            attention_mask_chunk = attention_mask[start:end]

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

            input_dict = {
                "input_ids": torch.tensor([input_ids_chunk], device=device).long(),
                "attention_mask": torch.tensor(
                    [attention_mask_chunk], device=device
                ).int(),
            }

            with torch.no_grad():
                outputs = self.trained_sent_pipeline.model(**input_dict)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=1)

            start = end
            proba_list.append(probabilities)
        return proba_list

    def get_tag_from_proba_absa(self, proba_list: List) -> tuple[str, list]:
        """Determines the sentiment tag and its associated probabilities from a list of probability tensors.

        Args:
            proba_list (List[torch.Tensor]): A list of probability tensors,
                where each tensor corresponds to the sentiment probabilities for a chunk of text.

        Returns:
            tuple[str, list]:
                - str: The predicted sentiment tag ("positive", "neutral", or "negative").
                - list: The mean probability values for each sentiment class:
                    - mean[0]: Probability of negative sentiment.
                    - mean[1]: Probability of neutral sentiment.
                    - mean[2]: Probability of positive sentiment.
        """
        # Ensures that gradients are not computed, saving memory
        with torch.no_grad():
            # Stack the list of tensors into a single tensor
            stacks = torch.stack(proba_list)
            # Compute the mean along the zeroth dimension (i.e., the chunk dimension)
            mean = stacks.mean(dim=0)[0]
            # get number tag
            num_tag = torch.argmax(mean).item()
            if num_tag == 2:
                tag = "positive"
            elif num_tag == 1:
                tag = "neutral"
            else:
                tag = "negative"
            return tag, mean

    # inference chunk function
    def inference(
        self,
        text: str,
        entities: Optional[List[Dict[str, Union[str, List]]]],
        window_length: int,
        device: str,
    ) -> dict:
        """Performs sentiment analysis on a given text and its associated entities.

        Args:
            text (str): The input text for sentiment analysis.
            entities (Optional[List[Dict[str, Union[str, List]]]]): A list of entities to analyze,
                where each entity is a dictionary containing 'entity_text' and optionally other metadata.
            window_length (int): The length of the sliding window used for token chunking during model inference.
            device (str): The device to perform the inference on (e.g., 'cpu' or 'cuda').

        Returns:
            dict: A dictionary containing:
                - "label" (str): The global sentiment label (e.g., "positive", "neutral", or "negative").
                - "negative_prob" (float): The probability of negative sentiment.
                - "positive_prob" (float): The probability of positive sentiment.
                - "entities" (Optional[List[Dict]]):
                    A list of entities with their respective sentiment labels added under the key "sentiment".
        """
        # initialize final result
        sentiment_result: Dict[str, Union[float, str, List[Any]]] = {}
        tokens = self.trained_sent_pipeline.tokenizer(text, add_special_tokens=False)
        # global sentiment
        global_aspect_tokens = self.trained_sent_pipeline.tokenizer(
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
            device=device,
        )
        global_tag, global_prob = self.get_tag_from_proba_absa(global_proba_list)
        sentiment_result["label"] = global_tag
        sentiment_result["negative_prob"] = round(global_prob[0].item(), 4)
        sentiment_result["positive_prob"] = round(global_prob[2].item(), 4)
        # entity sentiment
        if entities is not None and len(entities) > 0:
            entity_sentiment = []
            for entity in entities:
                try:
                    entity_text = entity.get("entity_text")
                    entity_tokens = self.trained_sent_pipeline.tokenizer(
                        entity_text, add_special_tokens=False
                    )
                    entity_proba_list = self.chunk_text_and_predict_proba_absa(
                        tokens["input_ids"],
                        tokens["attention_mask"],
                        entity_tokens["input_ids"],
                        entity_tokens["attention_mask"],
                        len(tokens["input_ids"]),
                        global_sentiment_tag=False,
                        window_length=window_length,
                        device=device,
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
        sentiment_output = self.inference(
            text=preprocessed_sentences,
            entities=entities,
            window_length=self.window_length,
            device=self.device,
        )
        return sentiment_output
