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
    prompt_ad_alias: str = "ml-transcript-segmentation-ad-detection"
    internal_ml_endpoint_api_key: str = "1234"
    default_model: str = "gpt-4-0125-preview"
    segmentation_output_schema: Dict[str, str] = {
        "related_segment": "The relevant news segment about the keywords",
        "reason_for_segment": "The reason you believe this story relates to the keywords",
        "segment_summary": "A one sentence summary of the segment extracted",
        "segment_title": "A title that represents the segment extracted. The title must be in same language as the segment.",  # noqa: E501
        "segment_amount": "How many news segment in total",
        "piece_before": "The piece before the chosen segment",
        "piece_after": "The piece after the chosen segment",
        "piece_before_accept": "Does the piece before the segment hold any relevance to the segment and keywords? You must answer with just Yes or No",  # noqa: E501
        "piece_after_accept": "Does the piece after the segment hold any relevance to the segment and keywords? You must answer with just Yes or No",  # noqa: E501
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
