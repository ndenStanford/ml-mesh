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

    def find_timestamps_from_word_transcript(
        self,
        segment: str,
        word_transcript: List[Dict[str, Any]],
        offset_start_buffer: float,
        offset_end_buffer: float,
    ) -> Tuple[
        Tuple[Union[int, float], Union[int, float]],
        Tuple[Union[int, float], Union[int, float]],
    ]:
        """Find timestamps by comparing segment to word-level transcript.

        Args:
            segment (str): segment from GPT
            word_transcript (List[Dict[str, Any]): Word-based transcript
            offset_start_buffer (float): start offset, float
            offset_end_buffer (float): end offset, float

        Returns:
            Tuple[
                Tuple[Union[int, float], Union[int, float]],
                Tuple[Union[int, float], Union[int, float]],
            ]:The start and end timestamp of the segment and offsetted timestamps
        """
        # Filter out entries with None values
        word_transcript_filtered = [i for i in word_transcript if i["w"] is not None]

        # Extract first and last portions of the segment
        segment_split = segment.split()

        THRESHOLD = 20

        first_portion = " ".join(segment_split[:THRESHOLD]).lstrip(">")
        last_portion = " ".join(segment_split[-THRESHOLD:]).lstrip(">")

        # Find the most compatible sublists that matches the portions from the segment
        max_similarity_start = 0
        max_similarity_end = 0
        best_portion_start = []
        best_portion_end: List[Dict[str, Any]] = []

        for i in range(len(word_transcript_filtered) - (THRESHOLD - 1)):
            candidate_list = word_transcript_filtered[i : i + THRESHOLD]  # noqa: E203
            candidate = " ".join([word["w"].lstrip(">") for word in candidate_list])
            # fix abbreviations
            candidate = candidate.replace(" .", ".")

            similarity_start = fuzz.ratio(candidate, first_portion)
            similarity_end = fuzz.ratio(candidate, last_portion)

            if (
                similarity_start > max_similarity_start
                and best_portion_end != candidate_list
            ):
                max_similarity_start = similarity_start
                best_portion_start = candidate_list

            if (
                similarity_end > max_similarity_end
                and best_portion_start != candidate_list
            ):
                max_similarity_end = similarity_end
                best_portion_end = candidate_list

        start_time = best_portion_start[0]["ts"]
        end_time = best_portion_end[-1]["ts"]
        start_time_offsetted = start_time + offset_start_buffer
        end_time_offsetted = end_time + offset_end_buffer

        if start_time_offsetted < word_transcript_filtered[0]["ts"]:
            start_time_offsetted = word_transcript_filtered[0]["ts"]

        if end_time_offsetted > word_transcript_filtered[-1]["ts"]:
            end_time_offsetted = word_transcript_filtered[-1]["ts"]

        return ((start_time, end_time), (start_time_offsetted, end_time_offsetted))

    def postprocess(
        self,
        response: Union[str, Dict[str, str]],
        word_transcript: List[Dict[str, Any]],
        offset_start_buffer: float,
        offset_end_buffer: float,
    ) -> Tuple[
        Tuple[Union[int, float], Union[int, float]],
        Tuple[Union[int, float], Union[int, float]],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        """Find timestamp by tracing content back to word transcript.

        Args:
            response Union[str, Dict[str, str]]: Response from GPT model
            word_transcript (List[Dict[str, Any]): Word-based transcript
            offset_start_buffer (float): start offset, float
            offset_end_buffer (float): end offset, float

        Returns:
            Tuple[
                Tuple[Union[int, float], Union[int, float]],
                Tuple[Union[int, float], Union[int, float]],
                Optional[str],
                Optional[str],
            ]:The start and end timestamp of the segment, the segment title, the segment summary.
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
            start_time, end_time, start_time_offsetted, end_time_offsetted, segment = (
                0.0,
                0.0,
                0.0,
                0.0,
                "",
            )
        else:
            (
                (start_time, end_time),
                (start_time_offsetted, end_time_offsetted),
            ) = self.find_timestamps_from_word_transcript(
                json_response[self.related_segment_key],
                word_transcript,
                offset_start_buffer,
                offset_end_buffer,
            )
            segment = json_response.get(self.related_segment_key)

        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            json_response.get("Segment title"),
            json_response.get("Segment summary"),
            segment,
        )

    def preprocess_transcript(self, word_transcript: List[Dict[str, Any]]) -> str:
        """Convert word-based transcript into paragraph.

        Args:
            word_transcript (List[Dict[str, Any]): Word-based transcript

        Returns:
            str: paragraph made out of word transcript
        """
        paragraph = " ".join(
            word["w"] for word in word_transcript if word.get("w") is not None
        ).strip()
        # merge abbreviations without spaces
        paragraph = paragraph.replace(" .", ".")
        return paragraph

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
        offset_start_buffer: float = -7000.0,
        offset_end_buffer: float = 5000.0,
    ) -> Tuple[
        Tuple[Union[int, float], Union[int, float]],
        Tuple[Union[int, float], Union[int, float]],
        Optional[str],
        Optional[str],
        Optional[str],
    ]:
        """Prediction method for transcript segmentation.

        Args:
            transcript (List[Dict[str, Any]]): Inputted word-based transcript
            keyword (List[str]): List of keywords to query the transcript
            offset_start_buffer (float): start offset, float
            offset_end_buffer (float): end offset, float

        Returns:
            Tuple[
                Tuple[Union[int, float], Union[int, float]],
                Tuple[Union[int, float], Union[int, float]],
                Optional[str],
                Optional[str],
            ]: Timestamps of the segment based on keywords and segment title.
        """
        # preprocess
        paragraph = self.preprocess_transcript(word_transcript)

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
            title,
            summary,
            segment,
        ) = self.postprocess(
            response=json.loads(q.content)["generated"],
            word_transcript=word_transcript,
            offset_start_buffer=offset_start_buffer,
            offset_end_buffer=offset_end_buffer,
        )

        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            title,
            summary,
            segment,
        )
