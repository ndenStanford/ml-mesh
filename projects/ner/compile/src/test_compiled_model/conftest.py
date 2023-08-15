# Standard Library
import json
from typing import Any, Dict, List, Union

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import LogFormat, get_default_logger
from onclusiveml.models.ner import CompiledNER

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompilationTestSettings,
    IOSettings,
)


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
def test_files_predictions() -> List[List[Dict[str, Union[str, int, float]]]]:
    return [
        [
            {
                "entity": "ORG",
                "score": 0.9981778860092163,
                "sentence_index": 0,
                "word": "Google",
                "start": 0,
                "end": 6,
            },
            {
                "entity": "LOC",
                "score": 0.998550146818161,
                "sentence_index": 0,
                "word": "Mountain View",
                "start": 16,
                "end": 29,
            },
            {
                "entity": "LOC",
                "score": 0.9993670582771301,
                "sentence_index": 0,
                "word": "CA",
                "start": 31,
                "end": 33,
            },
        ],
        [
            {
                "entity": "LOC",
                "score": 0.991286963224411,
                "sentence_index": 0,
                "word": "Gulf Stream",
                "start": 21,
                "end": 32,
            },
            {
                "entity": "LOC",
                "score": 0.9935731490453085,
                "sentence_index": 0,
                "word": "Cape Cod",
                "start": 81,
                "end": 89,
            },
        ],
        [
            {
                "entity": "LOC",
                "score": 0.9925467371940613,
                "sentence_index": 0,
                "word": "Jupiter",
                "start": 105,
                "end": 112,
            }
        ],
        [
            {
                "entity": "ORG",
                "score": 0.7017723023891449,
                "sentence_index": 0,
                "word": "Loggerhead Marinelife Center",
                "start": 10,
                "end": 38,
            }
        ],
    ]
