# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.tracking.tracked_model_version import TrackedModelVersion


@pytest.mark.parametrize(
    "local_directory_path, neptune_attribute_path",
    [
        (".", "some_attribute_path"),
        (".", "some/nested/attribute/path"),
        (".", ""),
        ("some_dir", "some_attribute"),
        ("some_dir", "some/nested/attribute/path"),
        ("some_dir", ""),
        (os.path.join("some", "nested", "dir"), "some_attribute"),
        (os.path.join("some", "nested", "dir"), "some/nested/attribute/path"),
        (os.path.join("some", "nested", "dir"), ""),
    ],
)
def test_capture_directory_for_upload(
    test_directory,
    monkeypatch,
    local_directory_path,
    neptune_attribute_path,
    test_captured_directories_for_upload_expected,
):
    def mock_walk(local_directory_path, topdown):
        return test_directory

    monkeypatch.setattr(os, "walk", mock_walk)

    test_captured_directories_for_upload_actual = (
        TrackedModelVersion.capture_directory_for_upload(
            local_directory_path=local_directory_path,
            neptune_attribute_path=neptune_attribute_path,
            exclude=(),
        )
    )

    test_captured_directories_for_upload_actual == test_captured_directories_for_upload_expected
