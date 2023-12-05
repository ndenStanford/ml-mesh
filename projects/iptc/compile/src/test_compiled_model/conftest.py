"""Conftest."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.models.iptc import CompiledIPTC

# Source
from src.settings import CompilationTestSettings, IOSettings


@pytest.fixture
def io_settings() -> IOSettings:
    """IO Settings."""
    return IOSettings()


@pytest.fixture
def compilation_test_settings() -> CompilationTestSettings:
    """Compilation settings fixture."""
    return CompilationTestSettings()


@pytest.fixture()
def logger(io_settings: IOSettings) -> Any:
    """Logger fixture."""
    return get_default_logger(
        name=__name__,
        fmt_level=OnclusiveLogMessageFormat.DETAILED.name,
        level=io_settings.log_level,
    )


@pytest.fixture
def compiled_iptc(io_settings: IOSettings) -> CompiledIPTC:
    """Compiled iptc model fixture."""
    # load compiled iptc from previous workflow component
    compiled_iptc = CompiledIPTC.from_pretrained(io_settings.compile.model_directory)

    return compiled_iptc


@pytest.fixture
def test_files(io_settings: IOSettings) -> Dict[str, Any]:
    """Test files fixtures."""
    # get test files & load directly into dict
    test_files = io_settings.download.test_files.copy()
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_files:
        with open(
            io_settings.download.test_files[test_file_reference], "r"
        ) as test_file:
            test_files[test_file_reference] = json.load(test_file)

    return test_files
