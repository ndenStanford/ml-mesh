"""Logging params."""

# 3rd party libraries
from pydantic import validator

# Internal libraries
from onclusiveml.core.base.params import Params
from onclusiveml.core.logging.constants import (
    DEBUG,
    VALID_LOG_LEVELS,
    OnclusiveLogMessageFormat,
    OnclusiveService,
)


class OnclusiveLogSettings(Params):
    """Environment variable entrypoint for `get_default_logger` method inputs."""

    service: str = OnclusiveService.DEFAULT.value
    level: int = DEBUG
    fmt_level: str = OnclusiveLogMessageFormat.SIMPLE.name
    json_format: bool = False

    @validator("level")
    def validate_level(value: int) -> int:
        """Validates the log level value against log levels defined in the `constants` module."""
        if value not in VALID_LOG_LEVELS:
            raise ValueError(
                f"Specified log level is not inside the valid range of log levels: "
                f"{VALID_LOG_LEVELS}"
            )

        return value

    @validator("fmt_level")
    def check_fmt_level(value: str) -> str:
        """Validates the log message formatting level against OnclusiveLogMessageFormat fields."""
        valid_log_message_formats = OnclusiveLogMessageFormat.list(names=True)

        if value not in valid_log_message_formats:
            raise ValueError(
                f"The specified log message format {value} is not among the valid"
                f" log message formats: {valid_log_message_formats}"
            )

        return value

    class Config:
        env_prefix = "onclusiveml_core_logging_config_"
