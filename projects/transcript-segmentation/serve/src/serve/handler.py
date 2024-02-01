"""Transcript Segmentation."""

# Standard Library
import json
from typing import Any, Dict, List, Tuple, Union

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
    ) -> Tuple[int, int]:
        """Find start and end index of sentence-level transcript.

        Args:
            json_response (str): GPT response containing the  segment
            sentence_transcript (List[Dict[str, Any]]): sentence-level transcript

        Returns:
            Tuple[int,int]: start and end index of sentence level transcript
        """
        start_string = self.sentence_tokenizer.tokenize(
            content=json_response["Related segment"]
        )["sentences"][0]
        end_string = self.sentence_tokenizer.tokenize(
            content=json_response["Related segment"]
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

        return start_index, end_index

    def offset_timestamps(
        self,
        start_time: Union[int, float],
        end_time: Union[int, float],
        transcript: List[Dict[str, Any]],
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """Add offset to start and end time stamps.

        Args:
            start_time (Union[int, float]): start time of segment
            end_time (Union[int, float]): end time of segment
            transcript (List[Dict[str, Any]]): Sentence level transcript

        Returns:
            Tuple[Union[int, float], Union[int, float]]: ofsetted start/end timestamp of segment
        """
        # check if start_time is larger than 0 to then do offsetting
        if start_time > 0:
            start_time_offset = start_time - settings.OFFSET_BUFFER
            # If the timestamp is beyond the clip, then set start_time stamp to beginning
            if start_time_offset < transcript[0]["start_time"]:
                start_time_offset = transcript[0]["start_time"]
        else:
            start_time_offset = start_time
        # check if end_time is larger than 0 to do offsetting
        if end_time > 0:
            end_time_offset = end_time + settings.OFFSET_BUFFER
            # If the timestamp is beyondf the clip, then set end_time stamp to end
            if end_time_offset > transcript[-1]["end_time"]:
                end_time_offset = transcript[-1]["end_time"]
        else:
            end_time_offset = end_time

        return (start_time_offset, end_time_offset)

    def postprocess(
        self,
        response: Union[str, Dict[str, str]],
        sentence_transcript: List[Dict[str, Any]],
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """Find timestamp by tracing content back to sentence transcript.

        Args:
            response Union[str, Dict[str, str]]: Response from GPT model
            sentence_transcript (List[Dict[str, Any]]): Sentence-level transcript

        Returns:
            Tuple[Union[int, float], Union[int, float]]: he start and end timestamp of the segment
        """
        if isinstance(response, str):
            str_response = self.remove_newlines(response)
            json_response = eval(str_response)
        elif isinstance(response, dict):
            json_response = response

        if json_response["Related segment"] in ["N/A", "", "nothing", "n/a", "Nothing"]:
            start_time, end_time = 0, 0
        else:
            start_time_index, end_time_index = self.get_timestamps_index(
                json_response, sentence_transcript
            )
            start_time = sentence_transcript[start_time_index]["start_time"]
            end_time = sentence_transcript[end_time_index]["end_time"]
        return (start_time, end_time)

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
            keyword (List[str]): List of keywords

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
    ) -> Tuple[Union[int, float], Union[int, float]]:
        """Prediction method for transcript segmentation.

        Args:
            transcript (List[Dict[str, Any]]): Inputted word-based transcript
            keyword (List[str]): List of keywords to query the transcript

        Returns:
            Tuple[Union[int, float], Union[int, float]]: Timestamps of the segment based on keywords
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
        start_time, end_time = self.postprocess(
            response=json.loads(q.content)["generated"],
            sentence_transcript=preprocessed_sentence_transcript,
        )

        start_time_offset, end_time_offset = self.offset_timestamps(
            start_time, end_time, preprocessed_sentence_transcript
        )

        return start_time_offset, end_time_offset
