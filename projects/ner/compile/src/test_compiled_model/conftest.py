"""Conftest."""

# Standard Library
import json
from typing import Any, Dict, List, Union

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.models.ner import CompiledNER

# Source
from src.settings import (  # type: ignore[attr-defined]
    CompilationTestSettings,
    IOSettings,
)


@pytest.fixture
def io_settings() -> IOSettings:
    """Fixture to provide IOSettings instance.

    Returns:
        IOSettings: Instance of IOSettings
    """
    return IOSettings()


@pytest.fixture
def compilation_test_settings() -> CompilationTestSettings:
    """Fixture to provide CompilationTestSettings instance.

    Returns:
        CompilationTestSettings: Instance of CompilationTestSettings
    """
    return CompilationTestSettings()


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
def compiled_ner(io_settings: IOSettings) -> CompiledNER:
    """Fixture to provide a compiled NER model instance.

    Args:
        io_settings (IOSettings): IOSettings instance

    Returns:
        CompiledNER: Compiled NER model instance
    """
    # load compiled NER from previous workflow component
    compiled_ner = CompiledNER.from_pretrained(io_settings.compile.model_directory)

    return compiled_ner


@pytest.fixture
def test_files(io_settings: IOSettings) -> Dict[str, Any]:
    """Fixture to provide test input files loaded into a dictionary.

    Args:
        io_settings (IOSettings): IOSettings instance

    Returns:
        Dict[str, Any]: Dictionary containing test files data
    """
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
def test_files_predictions() -> Dict[str, List[Dict[str, Union[str, int, float]]]]:
    """Fixture to provide expected test predictions for different projects as a dictionary.

    Returns:
        Dict[str, List[Dict[str, Union[str, int, float]]]]:
        Predictions for each project, with each prediction consisting of a list of dictionaries.

    NOTE: The handler merges inner and outer tags into one tag,
    so modify expected predictions accordingly.
    """
    result_en = [
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
    ]

    result_multilingual = [
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
    ]

    return {
        "onclusive/ner": result_en,
        "onclusive/ner-multilingual": result_multilingual,
    }
