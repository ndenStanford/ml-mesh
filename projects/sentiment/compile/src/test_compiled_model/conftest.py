# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.ner import CompiledNER

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
def compiled_ner(io_settings: IOSettings) -> CompiledNER:
    # load compiled NER from previous workflow component
    compiled_ner = CompiledNER.from_pretrained(io_settings.compile.model_directory)

    return compiled_ner


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
def indexed_test_input(test_files: dict, test_sample_index: int) -> Any:

    return test_files["inputs"][test_sample_index]


@pytest.fixture
def indexed_test_expected_prediction(test_files: dict, test_sample_index: int) -> Any:

    return test_files["prediction"][test_sample_index]
