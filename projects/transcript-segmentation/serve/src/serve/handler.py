"""Transcript Segmentation."""

# Standard Library
import json
from typing import Any, Dict, List, Tuple, Union

# 3rd party libraries
import requests

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import get_api_settings  # type: ignore[attr-defined]


settings = get_api_settings()
logger = get_default_logger(__name__)


class TranscriptSegmentationHandler:
    """Transcript Segmentation using prompt backend."""

    output_truncated: bool = False
    input_truncated: bool = False

    def find_last_occurrence(self, phrase: str, transcript: str) -> int:
        """Find index of the last mention of phrase.

        Args:
            phrase (str): Given phrase
            transcript (str): Stringified transcript

        Returns:
            int: Index of the last mentioned phrase
        """
        position = transcript.rfind(phrase)
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

    def get_timestamps(
        self, json_response: Dict[str, Dict[str, Union[str, float]]]
    ) -> Tuple[int, int]:
        """Extract start and end timestamp of segment.

        Args:
            json_response (Dict[Dict[str, Union[str, float]]]): GPT output as JSON
        Returns:
            Tuple[int, int]: start and end timestamp
        """
        timestamps = json_response["Related segment"]

        if "start_time" in timestamps.keys() and "end_time" in timestamps.keys():
            st_str = "start_time"
            end_str = "end_time"
        elif "Start time" in timestamps.keys() and "End time" in timestamps.keys():
            st_str = "Start time"
            end_str = "End time"
        else:
            st_str = "start"
            end_str = "end"

        return (int(timestamps[st_str]), int(timestamps[end_str]))

    def postprocess(
        self,
        response: Union[str, Dict[str, Any]],
    ) -> Tuple[int, int]:
        """Post process GPT's JSON like string output and return start and end timestamps.

        Args:
            response (Union[str, Dict[str, Any]): Response from GPT model
        Returns:
            Tuple[int, int]: the start and end timestamp of the segment
        """
        if isinstance(response, str):
            str_response = self.remove_newlines(response)
            json_response = eval(str_response)
        elif isinstance(response, dict):
            json_response = response

        start_time, end_time = self.get_timestamps(json_response)

        return (start_time, end_time)

    def truncate_transcript(
        self,
        preprocessed_sentence_transcript: List[Dict[str, Any]],
        threshold: int = 300000,
    ) -> List[Dict[str, Any]]:
        """Truncate transcript to fit into the model.

        Args:
            transcript (List[Dict[str, Any]]): Sentence-based transcript
            threshold (int): Max character length of transcript

        Returns:
            List[Dict[str, Any]]: Truncated transcript
        """
        str_sentence_transcript = str(preprocessed_sentence_transcript)
        self.input_truncated = False
        if len(str_sentence_transcript) > threshold:
            # Find last complete json object from the truncated transcript and close the list
            str_sentence_transcript = str_sentence_transcript[:threshold]
            position = self.find_last_occurrence(
                """, {\'start_time\':""", str_sentence_transcript
            )
            str_sentence_transcript = str_sentence_transcript[:position] + "]"
            self.input_truncated = True
        truncated_sentence_transcript = eval(str_sentence_transcript)
        return truncated_sentence_transcript

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
                if len(transcript_dict["content"]) > 0 and i > 0:
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

    def __call__(
        self,
        word_transcript: List[Dict[str, Any]],
        keywords: List[str],
    ) -> Tuple[Union[int, float], Union[int, float], bool]:
        """Prediction method for transcript segmentation.

        Args:
            transcript (List[Dict[str, Any]]): Inputted word-based transcript
            keyword (List[str]): List of keywords to query the transcript

        Returns:
            Tuple[List[Dict[str, Any]], bool, bool]: Timestamps of the segment based on keywords
        """
        # preprocess
        preprocessed_sentence_transcript = self.preprocess_transcript(word_transcript)

        # truncate
        truncated_sentence_transcript = self.truncate_transcript(
            preprocessed_sentence_transcript
        )

        for i in truncated_sentence_transcript:
            print(i)

        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}
        payload = {"transcript": truncated_sentence_transcript, "keywords": keywords}
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
        )

        return start_time, end_time, self.input_truncated
