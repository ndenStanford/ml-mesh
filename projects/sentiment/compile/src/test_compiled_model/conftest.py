# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.sentiment import CompiledSent

# Source
from src.settings import CompilationTestSettings, IOSettings


@pytest.fixture
def io_settings() -> IOSettings:

    return IOSettings()


@pytest.fixture
def compilation_test_settings() -> CompilationTestSettings:

    return CompilationTestSettings()


@pytest.fixture()
def logger(io_settings: IOSettings) -> Any:

    return get_default_logger(
        name=__name__, fmt=LogFormat.DETAILED.value, level=io_settings.log_level
    )


@pytest.fixture
def compiled_sent(io_settings: IOSettings) -> CompiledSent:
    # load compiled Sent from previous workflow component
    compiled_sent = CompiledSent.from_pretrained(io_settings.compile.model_directory)

    return compiled_sent


@pytest.fixture
def test_files(io_settings: IOSettings) -> Dict[str, Any]:
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
def test_atol() -> float:
    return 2e-02


@pytest.fixture
def test_rtol() -> float:
    return 1e-02
