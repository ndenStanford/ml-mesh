"""Logging params."""

# Standard Library
from typing import List

# 3rd party libraries
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging.constants import (
    DEBUG,
    LOG_LEVELS,
    OnclusiveLogMessageFormat,
    OnclusiveService,
)


class OnclusiveLogSettings(OnclusiveBaseSettings):
    """Environment variable entrypoint for `get_default_logger` method inputs."""

    service: OnclusiveService = OnclusiveService.DEFAULT
    level: int = DEBUG
    fmt_level: OnclusiveLogMessageFormat = OnclusiveLogMessageFormat.SIMPLE
    json_format: bool = False
    suppressed_logger_names: List[str] = [
        "urllib3",
        "s3transfer",
        "requests_oauthlib",
        "botocore",
        "boto3",
    ]
    disabled_logger_names: List[str] = [
        "bravado_core",
        "bravado.client",
        "swagger_spec_validator",
    ]

    @field_validator("level")
    def validate_level(value: int) -> int:
        """Validates the log level value against log levels defined in the `constants` module."""
        if value not in LOG_LEVELS:
            raise ValueError(
                f"Specified log level is not inside the valid range of log levels: "
                f"{LOG_LEVELS}"
            )

        return value

    @field_validator("fmt_level")
    def check_fmt_level(value: str) -> str:
        """Validates the log message formatting level against OnclusiveLogMessageFormat fields."""
        valid_log_message_formats = OnclusiveLogMessageFormat.members()

        if value not in valid_log_message_formats:
            raise ValueError(
                f"The specified log message format {value} is not among the valid"
                f" log message formats: {valid_log_message_formats}"
            )

        return value

    model_config = SettingsConfigDict(env_prefix="onclusiveml_core_logging_config_")
