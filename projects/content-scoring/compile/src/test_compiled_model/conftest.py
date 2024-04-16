"""Conftest."""

# Standard Library
from typing import Any, Dict, List

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)

# Source
from src.settings import IOSettings  # type: ignore[attr-defined]


@pytest.fixture
def io_settings() -> IOSettings:
    """Fixture to provide IOSettings instance.

    Returns:
        IOSettings: Instance of IOSettings
    """
    return IOSettings()


@pytest.fixture()
def logger(io_settings: IOSettings) -> Any:
    """Fixture to provide a logger instance.

    Args:
        io_settings (IOSettings): IOSettings

    Returns:
        Any: Logger instance
    """
    return get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )


@pytest.fixture
def test_files_inputs() -> Dict[str, List[float]]:
    """Fixture to provide inputs.

    Args:
        None

    Returns:
        input dictionary
    """
    return {
        "pagerank": [3.299923, 9.1, 9.4],
        "reach": [90, 2821568, 3614746],
        "score": [628226.6, 4213572.0, 1601918.4],
        "lang": [2.0, 2.0, 0.0],
        "media_type": [3.0, 3.0, 3.0],
        "label": [1.0, 1.0, 2.0],
        "publication": [72.0, 69.0, 43.0],
        "country": [1.0, 1.0, 2.0],
        "is_copyrighted": [0.0, 0.0, 0.0],
        "type_of_summary": [0.0, 0.0, 0.0],
    }


@pytest.fixture
def test_files_predictions() -> Dict[str, List[str]]:
    """Fixture to provide predictions.

    Args:
        None

    Returns:
        output dictionary
    """
    return {"boolean_messages": ["rejected", "rejected", "rejected"]}
