"""Transcript Segmentation."""

# Standard Library
import json
from json.decoder import JSONDecodeError
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

    def find_last_occurrence(self, phrase: str, response: str) -> int:
        """Find index of the last mention of phrase.

        Args:
            phrase (str): Given phrase
            response (str): Stringified json

        Returns:
            int: Index of the last mentioned phrase
        """
        position = response.rfind(phrase)
        return position

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

        segment_split = segment.split()
        window_threshold = min(len(segment_split), settings.WINDOW_THRESHOLD)

        first_portion = " ".join(segment_split[:window_threshold]).lstrip(">")

        search_last_portion = False
        if window_threshold >= settings.WINDOW_THRESHOLD:
            search_last_portion = True
            last_portion = " ".join(segment_split[-window_threshold:]).lstrip(">")
        max_similarity_start = 0
        max_similarity_end = 0
        best_portion_start = []
        best_portion_end: List[Dict[str, Any]] = []

        for i in range(len(word_transcript_filtered) - (window_threshold - 1)):
            candidate_list = word_transcript_filtered[
                i : i + window_threshold  # noqa: E203
            ]
            candidate = " ".join([word["w"].lstrip(">") for word in candidate_list])
            candidate = candidate.replace(" .", ".")

            similarity_start = fuzz.ratio(candidate, first_portion)
            if search_last_portion:
                similarity_end = fuzz.ratio(candidate, last_portion)

            if (
                similarity_start > max_similarity_start
                and best_portion_end != candidate_list
            ):
                max_similarity_start = similarity_start
                best_portion_start = candidate_list

            if search_last_portion:
                if (
                    similarity_end > max_similarity_end
                    and best_portion_start != candidate_list
                ):
                    max_similarity_end = similarity_end
                    best_portion_end = candidate_list

        start_time = best_portion_start[0]["ts"]
        end_time = (
            best_portion_end[-1]["ts"]
            if search_last_portion
            else best_portion_start[-1]["ts"]
        )

        start_time_offsetted = max(
            start_time + offset_start_buffer, word_transcript_filtered[0]["ts"]
        )
        end_time_offsetted = min(
            end_time + offset_end_buffer, word_transcript_filtered[-1]["ts"]
        )

        return ((start_time, end_time), (start_time_offsetted, end_time_offsetted))

    def trim_response(self, str_response: str) -> str:
        """Fix incomplete json by remove field that is incomplete.

        Args:
            str_response (str): incomplete json string response

        Returns:
            str: complete json string response
        """
        # reverse order of the json response
        fields_list = [
            ',  "Advertisement content": "',
            '",  "Piece after accept":"',
            '",  ["Piece after accept"]:"',
            '",  "Piece before accept":"',
            '",  ["Piece before accept"]:"',
            '",  "Piece after":"',
            '",  ["Piece after"]:"',
            '",  "Piece before":"',
            '",  ["Piece before"]:"',
            '",  "segment amount":"',
            '",  ["segment amount"]:"',
        ]
        for field in fields_list:
            position = self.find_last_occurrence(field, str_response)
            if position != -1:
                break
        return (
            str_response[:position] + "}"
            if position != -1
            else str_response[:position] + '"}'
        )

    def find_key(self, json_response: Dict[str, str], keys_list: List[str]) -> str:
        """Find the key that is being used in json response.

        Args:
            json_resposne (Dict[str,str]): openai json response
            keys_list: Candidate key that may be found in json response

        Returns:
            str: key that exists in json response
        """
        for key in keys_list:
            if key in json_response.keys():
                break
        return key

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
            try:
                json_response = eval(str_response)
            # Deal with issue where response is cutoff (finish_reason = length|content_filter)
            except SyntaxError:
                str_response = self.trim_response(str_response)
                json_response = eval(str_response)

        elif isinstance(response, dict):
            json_response = response
        # potential keys the gpt model could return
        related_seg_keys_list = [
            "Related segment",
            "Related Segment",
            "related_segment",
            "related segment",
            "segment",
            "Segment",
            "[Related segment]",
        ]
        self.related_segment_key = self.find_key(json_response, related_seg_keys_list)
        segment = json_response.get(self.related_segment_key)

        if segment in [
            "N/A",
            "",
            "nothing",
            "n/a",
            "Nothing",
            None,
        ]:
            (
                start_time,
                end_time,
                start_time_offsetted,
                end_time_offsetted,
                segment,
                segment_title,
                segment_summary,
            ) = (0.0, 0.0, 0.0, 0.0, "", None, None)
        else:

            piece_before_keys_list = [
                "Piece before",
                "piece before",
                "piece_before",
                "[Piece before]",
            ]
            self.piece_before_key = self.find_key(json_response, piece_before_keys_list)
            piece_before = json_response.get(self.piece_before_key)

            piece_after_keys_list = [
                "Piece after",
                "piece after",
                "piece_after",
                "[Piece after]",
            ]
            self.piece_after_key = self.find_key(json_response, piece_after_keys_list)
            piece_after = json_response.get(self.piece_after_key)

            piece_before_accept_keys_list = [
                "Piece before accept",
                "piece before accept",
                "Piece_before_accept",
                "[Piece before accept]",
            ]
            self.piece_before_accept_key = self.find_key(
                json_response, piece_before_accept_keys_list
            )
            piece_before_accept = json_response.get(self.piece_before_accept_key)

            piece_after_accept_keys_list = [
                "Piece after accept",
                "piece after accept",
                "Piece_after_accept",
                "[Piece after accept]",
            ]
            self.piece_after_accept_key = self.find_key(
                json_response, piece_after_accept_keys_list
            )
            piece_after_accept = json_response.get(self.piece_after_accept_key)

            segment_title_keys_list = [
                "Segment title",
                "segment title",
                "segment_title",
                "[Segment title]",
            ]
            self.segment_title_key = self.find_key(
                json_response, segment_title_keys_list
            )
            segment_title = json_response.get(self.segment_title_key)

            segment_summary_keys_list = [
                "Segment summary",
                "segment summary",
                "segment_summary",
                "[Segment summary]",
            ]
            self.segment_summary_key = self.find_key(
                json_response, segment_summary_keys_list
            )
            segment_summary = json_response.get(self.segment_summary_key)

            if piece_before_accept == "Yes":
                segment = piece_before + " " + segment

            if piece_after_accept == "Yes":
                segment = segment + piece_after

            (
                (start_time, end_time),
                (start_time_offsetted, end_time_offsetted),
            ) = self.find_timestamps_from_word_transcript(
                segment, word_transcript, offset_start_buffer, offset_end_buffer
            )

        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            segment_title,
            segment_summary,
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
            paragraph: combined content from transcript
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

    def ad_detect(self, paragraph: Optional[str]) -> Optional[bool]:
        """Detect the advertisement inside the selected transcript.

        Args:
            paragraph (str): transcript after postprocessing

        Return:
            Optional[bool]: True or False or None
        """
        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}
        payload = {
            "values": {
                "paragraph": paragraph,
            }
        }
        q = requests.post(
            "{}/api/v3/prompts/{}/generate/{}".format(
                settings.prompt_api_url,
                settings.prompt_ad_alias,
                settings.default_model,
            ),
            headers=headers,
            json=payload,
        )
        str_response = json.loads(q.content)["generated"]

        if isinstance(str_response, str):
            try:
                json_response = json.loads(str_response)
            except JSONDecodeError:
                str_response = self.remove_newlines(str_response)
                str_response = self.trim_response(str_response)
                json_response = json.loads(str_response)
        elif isinstance(str_response, dict):
            json_response = str_response
        # get the time stamp with ads
        candidate_keys = [
            "Advertisement detect",
            "[Advertisement detect]",
            "advertisement detect",
            "[advertisement detect]",
        ]

        advertisement_detect = "no"
        for key in candidate_keys:
            if isinstance(json_response.get(key), str):
                advertisement_detect = json_response.get(key).lower()
                break

        if advertisement_detect == "yes":
            return True
        else:
            return False

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
        Optional[bool],
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

        ad_detect_output = self.ad_detect(segment)

        return (
            (start_time_offsetted, end_time_offsetted),
            (start_time, end_time),
            title,
            summary,
            segment,
            ad_detect_output,
        )
