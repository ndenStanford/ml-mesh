"""Params test suite."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import OnclusiveLogSettings
from onclusiveml.core.logging.constants import (
    VALID_LOG_LEVELS,
    OnclusiveLogMessageFormat,
)


@pytest.mark.parametrize("level", VALID_LOG_LEVELS)
@pytest.mark.parametrize("fmt_level", OnclusiveLogMessageFormat.list(names=True))
@pytest.mark.parametrize("json_format", [True, False])
def test_onclusive_log_settings(level, fmt_level, json_format):
    """Tests the OnclusiveLogSettings constructor with all valid input configurations."""
    OnclusiveLogSettings(level=level, fmt_level=fmt_level, json_format=json_format)
