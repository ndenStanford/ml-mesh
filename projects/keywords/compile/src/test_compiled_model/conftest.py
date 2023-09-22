"""Conftest."""

# Standard Library
import json
from typing import Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.keywords import CompiledKeyBERT

# Source
from src.settings import CompilationTestSettings, CompilePipelineIOSettings


@pytest.fixture
def io_settings():
    """IO settings fixture."""
    return CompilePipelineIOSettings()


@pytest.fixture
def compilation_test_settings():
    """Compilation test settings fixture."""
    return CompilationTestSettings()


@pytest.fixture()
def logger(io_settings):
    """Logger settings fixture."""
    return get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.logger_level
    )


@pytest.fixture
def compiled_keybert(io_settings):
    """Compiled keybert fixture."""
    # load compiled keybert from previous workflow component
    compiled_keybert = CompiledKeyBERT.from_pretrained(
        io_settings.compile.model_directory
    )

    return compiled_keybert


@pytest.fixture
def test_files(io_settings) -> Dict:
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


@pytest.fixture
def indexed_test_input(test_files, test_sample_index: int):
    """Indexed test inputs fixture."""
    return test_files["inputs"][test_sample_index]


@pytest.fixture
def indexed_test_expected_prediction(test_files, test_sample_index: int):
    """Indexed test expected prediction fixture."""
    return test_files["prediction"][test_sample_index]
