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


@pytest.fixture(scope="session")
def settings() -> OnclusiveBaseSettings:
    """Fixture to provide IOSettings instance.

    Returns:
        IOSettings: Instance of IOSettings
    """
    return get_settings()


@pytest.fixture(scope="session")
def compiled_ner(settings: OnclusiveBaseSettings) -> CompiledNER:
    """Fixture to provide a compiled NER model instance.

    Args:
        settings (IOSettings): IOSettings instance
    Returns:
        CompiledNER: Compiled NER model instance
    """
    target_model_directory: str = os.path.join(
        "./outputs", "compile", "model_artifacts"
    )

    compiled_ner = CompiledNER.from_pretrained(target_model_directory)

    return compiled_ner


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
                    "score": 0.9916256070137024,
                    "entity_text": "Google HQ",
                    "start": 0,
                    "end": 9,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9991127848625183,
                    "entity_text": "Mountain View",
                    "start": 16,
                    "end": 29,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9996210336685181,
                    "entity_text": "CA",
                    "start": 31,
                    "end": 33,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9992565661668777,
                    "entity_text": "Gulf Stream",
                    "start": 21,
                    "end": 32,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9996319115161896,
                    "entity_text": "Cape Cod",
                    "start": 81,
                    "end": 89,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9997443556785583,
                    "entity_text": "Jupiter",
                    "start": 105,
                    "end": 112,
                    "sentence_index": 0,
                }
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9641428589820862,
                    "entity_text": "Logg",
                    "start": 10,
                    "end": 14,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9843780994415283,
                    "entity_text": "erhead Marinelife Center",
                    "start": 14,
                    "end": 38,
                    "sentence_index": 0,
                },
            ],
        ],
        [
            [
                {
                    "entity_type": "ORG",
                    "score": 0.9996895790100098,
                    "entity_text": "Google",
                    "start": 0,
                    "end": 6,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9972768723964691,
                    "entity_text": "カリフォルニア州",
                    "start": 10,
                    "end": 18,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9834852814674377,
                    "entity_text": "マウンテンビュー",
                    "start": 18,
                    "end": 26,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9991763383150101,
                    "entity_text": "メキシコ",
                    "start": 0,
                    "end": 4,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9930540770292282,
                    "entity_text": "ケープコッド",
                    "start": 35,
                    "end": 41,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.9969054758548737,
                    "entity_text": "런던",
                    "start": 0,
                    "end": 2,
                    "sentence_index": 0,
                },
                {
                    "entity_type": "LOC",
                    "score": 0.9979509472846985,
                    "entity_text": "샌프란시스코",
                    "start": 4,
                    "end": 10,
                    "sentence_index": 0,
                },
            ],
            [
                {
                    "entity_type": "LOC",
                    "score": 0.997836838165919,
                    "entity_text": "Loggerhead Marinelife Center",
                    "start": 17,
                    "end": 45,
                    "sentence_index": 0,
                }
            ],
        ],
    ]
