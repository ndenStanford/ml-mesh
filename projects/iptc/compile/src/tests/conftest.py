"""Conftest."""

# Standard Library
import json
from typing import Any, Dict

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.compile.constants import CompileWorkflowTasks
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.logging import (
    OnclusiveLogMessageFormat,
    get_default_logger,
)
from onclusiveml.models.iptc import CompiledIPTC
from onclusiveml.models.iptc.class_dict import CLASS_DICT, ID_TO_TOPIC
from onclusiveml.models.iptc.test_samples import TEST_SAMPLES

# Source
from src.settings import get_settings


@pytest.fixture
def settings() -> OnclusiveBaseSettings:
    """IO Settings."""
    return get_settings()


@pytest.fixture()
def logger(settings: OnclusiveBaseSettings) -> Any:
    """Logger fixture."""
    return get_default_logger(
        name=__name__, fmt_level=OnclusiveLogMessageFormat.DETAILED
    )


@pytest.fixture
def compiled_iptc(settings: OnclusiveBaseSettings) -> CompiledIPTC:
    """Compiled iptc model fixture."""
    # load compiled iptc from previous workflow component
    compiled_iptc = CompiledIPTC.from_pretrained(
        settings.project, settings.model_directory(CompileWorkflowTasks.COMPILE)
    )

    return compiled_iptc


@pytest.fixture
def test_files(settings: OnclusiveBaseSettings) -> Dict[str, Any]:
    """Test files fixtures."""
    # get test files & load directly into dict
    test_files = settings.test_files(CompileWorkflowTasks.DOWNLOAD)
    # 'inputs', 'inference_params' & 'predictions'
    for test_file_reference in test_files:
        with open(
            settings.test_files(CompileWorkflowTasks.DOWNLOAD)[test_file_reference], "r"
        ) as test_file:
            test_files[test_file_reference] = json.load(test_file)

    return test_files


@pytest.fixture(scope="module")
def test_samples():
    """Test samples fixtures."""
    return TEST_SAMPLES


@pytest.fixture(scope="module")
def class_dict():
    """Class dict fixtures."""
    return CLASS_DICT


@pytest.fixture(scope="module")
def id_to_topic():
    """Id to topic fixtures."""
    return ID_TO_TOPIC
