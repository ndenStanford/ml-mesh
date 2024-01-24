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

        print()
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
        headers = {"x-api-key": settings.internal_ml_endpoint_api_key}
        payload = {"transcript": word_transcript, "keywords": keywords}
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
