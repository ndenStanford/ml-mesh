"""Transcript Segmentation."""

# Standard Library
import json
from typing import Any, Dict, List, Optional, Tuple, Union

# 3rd party libraries
import requests
from fuzzywuzzy import fuzz

# Internal libraries
from onclusiveml.core.logging import get_default_logger
from onclusiveml.nlp.sentence_tokenize import SentenceTokenizer

# Source
from src.settings import get_api_settings  # type: ignore[attr-defined]


settings = get_api_settings()
logger = get_default_logger(__name__)


class TranscriptSegmentationHandler:
    """Transcript Segmentation using prompt backend."""

    sentence_tokenizer: SentenceTokenizer = SentenceTokenizer()

    related_segment_key: str

    def remove_newlines(self, response: str) -> str:
        """Remove new lines from the string.

        Args:
            response (str): Stringified JSON from GPT

        Returns:
            str: Stringified JSON without new lines
        """
        response = response.replace("\n    ", "")
        response = response.replace("\n", "")
        return response

    def get_timestamps_index(
        self, json_response: Dict[str, str], sentence_transcript: List[Dict[str, Any]]
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Find start and end index of sentence-level transcript.

        Args:
            json_response (str): GPT response containing the  segment
            sentence_transcript (List[Dict[str, Any]]): sentence-level transcript

        Returns:
            Tuple[Tuple[int,int],Tuple[int,int]]: return original and offsetted start and end index
                of segment
        """
        start_string = self.sentence_tokenizer.tokenize(
            content=json_response[self.related_segment_key]
        )["sentences"][0]
        end_string = self.sentence_tokenizer.tokenize(
            content=json_response[self.related_segment_key]
        )["sentences"][-1]
        max_similarity_start = 0
        max_similarity_end = 0
        start_index = 0
        end_index = 0
        for idx, item in enumerate(sentence_transcript):
            sentence = item.get("content", "")
            similarity = fuzz.ratio(start_string, sentence)
            if similarity > max_similarity_start:
                max_similarity_start = similarity
                start_index = idx

        for idx, item in enumerate(sentence_transcript):
            sentence = item.get("content", "")
            similarity = fuzz.ratio(end_string, sentence)
            # in order to avoid capturing end time
            if similarity > max_similarity_end and (
                (idx > start_index)
                or (start_string == end_string and idx == start_index)
            ):
                max_similarity_end = similarity
                end_index = idx

        # expand segment by adding extra sentences on both sides of segment
        start_index_offsetted = start_index - settings.OFFSET_INDEX_BUFFER
        end_index_offsetted = end_index + settings.OFFSET_INDEX_BUFFER

        # ensure the offsetted indexes do not go out of range
        if start_index_offsetted < 0:
            start_index_offsetted = 0
        if end_index_offsetted > len(sentence_transcript) - 1:
            end_index_offsetted = len(sentence_transcript) - 1

        return ((start_index_offsetted, end_index_offsetted), (start_index, end_index))

    def postprocess(
        self,
        response: Union[str, Dict[str, str]],
        sentence_transcript: List[Dict[str, Any]],
    ) -> Tuple[
        Tuple[Union[int, float], Union[int, float]],
        Tuple[Union[int, float], Union[int, float]],
        Optional[str],
    ]:
        """Find timestamp by tracing content back to sentence transcript.

        Args:
            response Union[str, Dict[str, str]]: Response from GPT model
            sentence_transcript (List[Dict[str, Any]]): Sentence-level transcript

        Returns:
            Tuple[
                Tuple[Union[int, float], Union[int, float]],
                Tuple[Union[int, float], Union[int, float]],
                Optional[str],
            ]:The start and end timestamp of the segment and the segment summary.
        """
        if isinstance(response, str):
            str_response = self.remove_newlines(response)
            json_response = eval(str_response)
        elif isinstance(response, dict):
            json_response = response

        # potential keys the gpt model could return
        if "Related segment" in json_response.keys():
            self.related_segment_key = "Related segment"
        elif "Related Segment" in json_response.keys():
            self.related_segment_key = "Related Segment"
        elif "related_segment" in json_response.keys():
            self.related_segment_key = "related_segment"
        elif "segment" in json_response.keys():
            self.related_segment_key = "segment"
        elif "Segment" in json_response.keys():
            self.related_segment_key = "Segment"

        if json_response[self.related_segment_key] in [
            "N/A",
            "",
            "nothing",
            "n/a",
            "Nothing",
        ]:
            start_time, end_time = 0, 0
        else:
            (
                (start_index_offsetted, end_index_offsetted),
                (start_index, end_index),
            ) = self.get_timestamps_index(json_response, sentence_transcript)
            # find timestamp from sentence level transcript
            start_time_offsetted = sentence_transcript[start_index_offsetted][
                "start_time"
            ]
            end_time_offsetted = sentence_transcript[end_index_offsetted]["end_time"]
            start_time = sentence_transcript[start_index]["start_time"]
            end_time = sentence_transcript[end_index]["end_time"]
        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            json_response.get("Segment summary"),
        )

    def preprocess_transcript(
        self, word_transcript: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Convert word-based transcript into sentence-based.

        Args:
            word_transcript (List[Dict[str, Any]): Word-based transcript

        Returns:
            List[Dict[str, Any]: Transcript converted into sentences
        """
        transcript_preprocessed = []
        transcript_dict: Dict[str, Any] = {}
        # Iterate over each word from word based transcript and merge into sentences
        for i in range(len(word_transcript)):
            if word_transcript[i]["w"] is not None:
                if not transcript_dict:
                    transcript_dict["start_time"] = word_transcript[i]["ts"]
                if "content" not in transcript_dict:
                    transcript_dict["content"] = str(
                        word_transcript[i]["w"]
                    )  # Convert to string
                else:
                    # merge abreviations without spaces
                    if (
                        len(word_transcript[i]["w"]) == 2
                        and word_transcript[i]["w"][-1] == "."
                        and len(word_transcript[i - 1]["w"]) == 2
                        and word_transcript[i - 1]["w"][-1] == "."
                    ):
                        transcript_dict["content"] += str(
                            word_transcript[i]["w"]
                        )  # Convert to string
                    else:
                        transcript_dict["content"] += " " + str(
                            word_transcript[i]["w"]
                        )  # Convert to string
                if len(transcript_dict["content"]) > 0:
                    # If contain certain punctuation, complete the sentence and start new sentence
                    if len(str(word_transcript[i]["w"])) != 2 and transcript_dict[
                        "content"
                    ][-1] in [".", "!", "?"]:
                        transcript_dict["end_time"] = word_transcript[i]["ts"]
                        transcript_preprocessed.append(transcript_dict)
                        transcript_dict = {}
        # append left over transcript at the end
        if transcript_dict:
            if len(transcript_dict["content"]) > 0:
                transcript_dict["end_time"] = word_transcript[i]["ts"]
                transcript_preprocessed.append(transcript_dict)
                transcript_dict = {}
        return transcript_preprocessed

    def create_paragraph(self, sentence_transcript: List[Dict[str, Any]]) -> str:
        """Merge sentences into paragraphs which will be fed to gpt model, excludes timestamps.

        Args:
            sentence_transcript List[Dict[str, Any]]: sentence-level transcript

        Returns:
            str: string extract of transcript
        """
        return " ".join(list(map(lambda x: x["content"], sentence_transcript)))

    def trim_paragraph(self, paragraph: str, keywords: List[str]) -> str:
        """Trime paragraph to focus on keywords.

        Args:
            paragraph: combined content from sentence transcript
            keywords (List[str]): List of keywords

        Returns:
            str: trimmeded paragraph

        note:
        """
        # truncates the paragraph such that it focuses more on the keywords
        # This is to avoid "lost in the middle" phenomena which is a big problem with LLMs
        beg, end = len(paragraph), 0
        lowercase_paragraph = paragraph.lower()
        indices = [
            (lowercase_paragraph.find(k.lower()), lowercase_paragraph.rfind(k.lower()))
            for k in keywords
        ]
        beg = min(
            filter(lambda x: 0 < x[0] < beg or (x[0] > 0 and beg == -1), indices),
            default=(len(paragraph), 0),
        )[0]
        end = max((e_temp for _, e_temp in indices), default=0)

        beg = max(0, beg - settings.CHARACTER_BUFFER)
        end = end + settings.CHARACTER_BUFFER if end > 0 else len(paragraph)
        return paragraph[beg:end]

    def __call__(
        self,
        word_transcript: List[Dict[str, Any]],
        keywords: List[str],
    ) -> Tuple[
        Tuple[Union[int, float], Union[int, float]],
        Tuple[Union[int, float], Union[int, float]],
        Optional[str],
    ]:
        """Prediction method for transcript segmentation.

        Args:
            transcript (List[Dict[str, Any]]): Inputted word-based transcript
            keyword (List[str]): List of keywords to query the transcript

        Returns:
            Tuple[
                Tuple[Union[int, float], Union[int, float]],
                Tuple[Union[int, float], Union[int, float]],
                Optional[str],
            ]: Timestamps of the segment based on keywords and segment summary.
        """
        # preprocess
        preprocessed_sentence_transcript = self.preprocess_transcript(word_transcript)

        # preprocess paragraph
        paragraph = self.create_paragraph(preprocessed_sentence_transcript)

        # Truncate paragraph
        trimmed_paragraph = self.trim_paragraph(paragraph, keywords)

        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}
        payload = {"paragraph": trimmed_paragraph, "keywords": keywords}
        q = requests.post(
            "{}/api/v1/prompts/{}/generate".format(
                settings.prompt_api_url, settings.prompt_alias
            ),
            headers=headers,
            json=payload,
        )

        # post process
        (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            summary,
        ) = self.postprocess(
            response=json.loads(q.content)["generated"],
            sentence_transcript=preprocessed_sentence_transcript,
        )

        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            summary,
        )
