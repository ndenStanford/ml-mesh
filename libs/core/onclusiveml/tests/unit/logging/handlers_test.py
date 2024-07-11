"""Handlers test suite."""

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveFormatter,
    OnclusiveJSONFormatter,
    get_default_handler,
)
from onclusiveml.core.logging.constants import (
    LOG_LEVELS,
    OnclusiveLogMessageFormat,
)


@pytest.mark.parametrize("level", LOG_LEVELS)
@pytest.mark.parametrize("fmt_level", OnclusiveLogMessageFormat.members())
@pytest.mark.parametrize("json_format", [True, False])
def test_get_default_handler(level, fmt_level, json_format):
    """Tests the get_default_handler method with all valid input configurations."""
    handler = get_default_handler(
        service="test-service",
        level=level,
        fmt_level=fmt_level,
        json_format=json_format,
    )

    assert handler.level == level
    assert handler.formatter._style._fmt == fmt_level.value

    if json_format:
        assert isinstance(handler.formatter, OnclusiveJSONFormatter)
    else:
        assert isinstance(handler.formatter, OnclusiveFormatter)

    assert handler.formatter.service == "test-service"
