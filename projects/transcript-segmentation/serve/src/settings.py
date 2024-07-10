"""Settings."""

# Standard Library
from functools import lru_cache
from typing import Dict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings, OnclusiveFrozenSettings
from onclusiveml.serving.rest.serve.params import ServingParams
from onclusiveml.tracking import TrackedGithubActionsSpecs, TrackedImageSpecs


class ServerModelSettings(ServingParams):
    """Serve model parameters."""

    model_name: str = "transcript-segmentation"


class PromptBackendAPISettings(OnclusiveFrozenSettings):
    """API configuration."""

    prompt_api_url: str = "http://prompt-backend:4000"
    prompt_alias: str = "ml-transcript-segmentation"
    prompt_ad_alias: str = "ml-transcript-segmentation-ad-detection-claude"
    internal_ml_endpoint_api_key: str = "1234"
    default_model_segmentation: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    default_model_ad: str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    segmentation_output_schema: Dict[str, str] = {
        "related_segment": "The most descriptive and informative news segment related to the keywords (DO NOT MODIFY THE TEXT IN ANY WAY, INCLUDING SPELLING, PUNCTUATION, ETC.)",  # noqa: E501
        "reason_for_segment": "The reason you believe this story relates to the keywords",
        "segment_summary": "A one-sentence summary of the extracted segment in the same language as the segment",  # noqa: E501
        "segment_title": "A title that represents the extracted segment in the same language as the segment",  # noqa: E501
        "segment_amount": "The total number of news segments in the content",
        "piece_before": "The segment immediately before the chosen segment (DO NOT MODIFY THE TEXT IN ANY WAY, INCLUDING SPELLING, PUNCTUATION, ETC.)",  # noqa: E501
        "piece_after": "The segment immediately after the chosen segment (DO NOT MODIFY THE TEXT IN ANY WAY, INCLUDING SPELLING, PUNCTUATION, ETC.)",  # noqa: E501
        "piece_before_accept": "Yes/No - Does the piece before hold any relevance to the segment and keywords?",  # noqa: E501
        "piece_after_accept": "Yes/No - Does the piece after hold any relevance to the segment and keywords?",  # noqa: E501
    }
    ad_detection_output_schema: Dict[str, str] = {
        "advertisement_detect": "Answer 'yes' or 'no' to indicate if there is any advertisement in the paragraph",  # noqa: E501
        "advertisement_content": "The reason for why you think there is advertisement",
    }


class TranscriptSegmentationHandlerSettings(OnclusiveBaseSettings):
    """Transcript Segmentation configurations."""

    CHARACTER_BUFFER: int = 2500
    WINDOW_THRESHOLD: int = 20


class GlobalSettings(
    ServerModelSettings,
    TrackedGithubActionsSpecs,
    TrackedImageSpecs,
):
    """Global server settings."""


class ApiSettings(
    PromptBackendAPISettings,
    TranscriptSegmentationHandlerSettings,
):
    """API settings."""


@lru_cache
def get_settings() -> OnclusiveFrozenSettings:
    """Returns instanciated global settings class."""
    return GlobalSettings()


@lru_cache
def get_api_settings() -> OnclusiveFrozenSettings:
    """Returns API settings."""
    return ApiSettings()
