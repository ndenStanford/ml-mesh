"""Conftest."""

# Standard Library
import os
from typing import Any, List

# 3rd party libraries
import pytest
from neptune.attributes.atoms.artifact import Artifact
from neptune.attributes.atoms.file import File


@pytest.fixture
def test_directory(local_directory_path: str):
    """Test directory fixture.

    {local_directory}
    |___'dir_1'
        |___dir_1_1
            |___file_1_1_1
        |___'file_1_1'
        |___'.file_1_2'
        |___'__file_1_3'
    |___'.dir_2'
        |___'file_2_1'
    |___'__dir_3'
        |___'file_3_1'

    """
    return [
        [local_directory_path, ["dir_1", ".dir_2", "__dir_3"], []],
        [
            f"{local_directory_path}/dir_1",
            ["dir_1_1"],
            ["file_1_1", ".file_1_2", "__file_1_3"],
        ],
        [f"{local_directory_path}/dir_1/dir_1_1", [], ["file_1_1_1"]],
        [f"{local_directory_path}/.dir_2", [], ["file_2_1"]],
        [f"{local_directory_path}/__dir_3", [], ["file_3_1"]],
    ]


@pytest.fixture
def test_captured_directories_for_upload_expected(
    local_directory_path: str, neptune_attribute_path: str
):
    """Test captured directories."""
    neptune_attribute_path_ext = (
        "" if not neptune_attribute_path else f"{neptune_attribute_path}/"
    )

    return [
        (
            os.path.join(local_directory_path, "dir_1", "file_1_1"),
            f"{neptune_attribute_path_ext}dir_1/file_1_1",
        ),
        (
            os.path.join(local_directory_path, "dir_1", ".file_1_2"),
            f"{neptune_attribute_path_ext}dir_1/.file_1_2",
        ),
        (
            os.path.join(local_directory_path, "dir_1", "__file_1_3"),
            f"{neptune_attribute_path_ext}dir_1/__file_1_3",
        ),
        (
            os.path.join(local_directory_path, "dir_1", "dir_1_1", "file_1_1_1"),
            f"{neptune_attribute_path_ext}dir_1/dir_1_1/file_1_1_1",
        ),
        (
            os.path.join(local_directory_path, ".dir_2", "file_2_1"),
            f"{neptune_attribute_path_ext}.dir_2/file_2_1",
        ),
        (
            os.path.join(local_directory_path, "dir_3", "file_3_1"),
            f"{neptune_attribute_path_ext}__dir_3/file_3_1",
        ),
    ]


def test_file(path: List[Any]):
    """Test file."""
    return File(container=[], path=path)


def test_artifact(path: List[Any]):
    """Test artifact."""
    return Artifact(container=[], path=path)


@pytest.fixture
def test_uploaded_attributes():
    """Test uploaded attributes."""
    return {
        "a": 1,
        "b": test_file(["b"]),
        "c": {
            "d": {"e": test_artifact(path=["c", "d", "e"]), "f": 2},
            "g": test_file(path=["c", "g"]),
        },
    }


@pytest.fixture
def test_extracted_data_attributes_expected():
    """Extracted data attributes fixture."""
    return [test_file(["b"]), test_artifact(["c", "d", "e"]), test_file(["c", "g"])]


@pytest.fixture
def test_derive_and_filter_neptune_attribute_paths_expected(neptune_attribute_prefix):
    """Derive and filter neptune attribute paths."""
    result = ["c/d/e", "c/g"]

    if neptune_attribute_prefix == "c":
        return result
    elif neptune_attribute_prefix == "":
        result.insert(0, "b")
        return result
    else:
        raise ValueError('Only values "c" and "" are suppported by this fixture.')
