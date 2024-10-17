"""Conftest."""

# Standard Library
import json
import os
from typing import Any, Dict, List, Union

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile.constants import CompileWorkflowTasks
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import OnclusiveLogSettings, get_default_logger
from onclusiveml.models.ner import CompiledNER

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompilationTestSettings,
    get_settings,
)


test_sample_indices = [0, 1, 2, 3]
languages = ["en", "ja"]
# Generate the parameter combinations using a list comprehension
parametrize_values = [
    (index, language, languages.index(language))
    for language in languages
    for index in test_sample_indices
]


@pytest.fixture
def settings() -> OnclusiveBaseSettings:
    """Fixture to provide IOSettings instance.

    Returns:
        IOSettings: Instance of IOSettings
    """
    return get_settings()


@pytest.fixture
def compilation_test_settings() -> CompilationTestSettings:
    """Fixture to provide CompilationTestSettings instance.

    Returns:
        CompilationTestSettings: Instance of CompilationTestSettings
    """
    return CompilationTestSettings()


@pytest.fixture()
def logger(settings: OnclusiveBaseSettings) -> Any:
    """Fixture to provide a logger instance.

    Args:
        io_settings (IOSettings): IOSettings

    Returns:
        Any: Logger instance
    """
    logging_settings = cast(settings, OnclusiveLogSettings)
    return get_default_logger(
        name=__name__,
        fmt_level=logging_settings.fmt_level,
    )


@pytest.fixture
def compiled_ner(settings: OnclusiveBaseSettings) -> CompiledNER:
    """Fixture to provide a compiled NER model instance.

    Args:
        io_settings (IOSettings): IOSettings instance

    Returns:
        CompiledNER: Compiled NER model instance
    """
    target_model_directory: str = os.path.join(
        "./outputs", "compile", "model_artifacts"
    )

    compiled_ner = CompiledNER.from_pretrained(target_model_directory)

    return compiled_ner


@pytest.fixture
def test_files(settings: OnclusiveBaseSettings) -> Dict[str, Any]:
    """Fixture to provide test input files loaded into a dictionary.

    Args:
        io_settings (IOSettings): IOSettings instance

    Returns:
        Dict[str, Any]: Dictionary containing test files data
    """
    # get test files & load directly into dict
    test_files = settings.test_files(CompileWorkflowTasks.DOWNLOAD)
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_files:
        with open(
            settings.test_files(CompileWorkflowTasks.DOWNLOAD)[test_file_reference], "r"
        ) as test_file:
            test_files[test_file_reference] = json.load(test_file)

    return test_files


@pytest.fixture
def test_files_predictions() -> List[List[Dict[str, Union[str, int, float]]]]:
    """Fixture to provide expected test predictions as a list of dictionaries.

    Returns:
        List[List[Dict[str, Union[str, int, float]]]]: Predictions in form of list of dictionaries
    NOTE: handler makes changes to the output by merging inner and outer tags
    into one tag and so modify expected predictions here
    """
    return [
        [
            [
                {
                    "entity_type": "ORG",
                    "score": 0.9981784820556641,
                    "sentence_index": 0,
                    "entity_text": "Google",
                    "start": 0,
                    "end": 6,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9985500276088715,
                    "sentence_index": 0,
                    "entity_text": "Mountain View",
                    "start": 16,
                    "end": 29,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9993670582771301,
                    "sentence_index": 0,
                    "entity_text": "CA",
                    "start": 31,
                    "end": 33,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.991286963224411,
                    "sentence_index": 0,
                    "entity_text": "Gulf Stream",
                    "start": 21,
                    "end": 32,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9935731490453085,
                    "sentence_index": 0,
                    "entity_text": "Cape Cod",
                    "start": 81,
                    "end": 89,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9925467371940613,
                    "sentence_index": 0,
                    "entity_text": "Jupiter",
                    "start": 105,
                    "end": 112,
                }
            ],
            [
                {
                    "entity_type": "ORG",
                    "score": 0.7017723023891449,
                    "sentence_index": 0,
                    "entity_text": "Loggerhead Marinelife Center",
                    "start": 10,
                    "end": 38,
                }
            ],
        ],
        [
            [
                {
                    "entity_type": "ORG",
                    "score": 0.9998427629470825,
                    "entity_text": "Google",
                    "start": 0,
                    "end": 6,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9976749370495478,
                    "entity_text": "カリフォルニアウンテンビュー",
                    "start": 10,
                    "end": 26,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.998959994316101,
                    "entity_text": "メキシコ",
                    "start": 0,
                    "end": 5,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "PER",
                    "score": 0.9701058566570282,
                    "entity_text": "ウミガメ",
                    "start": 19,
                    "end": 23,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.998335987329483,
                    "entity_text": "런던",
                    "start": 0,
                    "end": 2,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.999501903851827,
                    "entity_text": "샌프란시스코",
                    "start": 4,
                    "end": 10,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "ORG",
                    "score": 0.9580032527446747,
                    "entity_text": "Loggerhead Marinelife Center",
                    "start": 17,
                    "end": 45,
                    "sentence_index": 0,
                }
            ],
        ],
    ]
