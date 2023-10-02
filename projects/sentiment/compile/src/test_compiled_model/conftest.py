"""Conftest."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.sentiment import CompiledSent

# Source
from src.settings import CompilationTestSettings, CompilePipelineIOSettings


@pytest.fixture
def io_settings() -> CompilePipelineIOSettings:
    """Compile pipeline IO Settings."""
    return CompilePipelineIOSettings()


@pytest.fixture
def compilation_test_settings() -> CompilationTestSettings:
    """Compilation settings fixture."""
    return CompilationTestSettings()


@pytest.fixture()
def logger(io_settings: CompilePipelineIOSettings) -> Any:
    """Logger fixture."""
    return get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.logger_level
    )


@pytest.fixture
def compiled_sent(io_settings: CompilePipelineIOSettings) -> CompiledSent:
    """Compiled sentiment model fixture."""
    # load compiled Sent from previous workflow component
    compiled_sent = CompiledSent.from_pretrained(io_settings.compile.model_directory)

    return compiled_sent


@pytest.fixture
def test_files(io_settings: CompilePipelineIOSettings) -> Dict[str, Any]:
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
