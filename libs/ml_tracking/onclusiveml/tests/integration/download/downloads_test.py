# Standard Library
import os
import shutil

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.ml_tracking.download import (
    download_config_from_model_version,
    download_directory_from_model_version,
    download_file_from_model_version,
)
from onclusiveml.ml_tracking.upload import capture_directory_for_upload


@pytest.mark.order(2)
@pytest.mark.download
@pytest.mark.parametrize("test_model_version_mode", ["read-only"])
@pytest.mark.parametrize(
    "file_name,file_extension",
    [
        ("test_file_1", "json"),
        ("test_file_2", "txt"),
    ],
)
def download_file_from_model_version_test(
    test_model_version,
    test_model_version_mode,
    test_file_directory_download,
    file_name,
    file_extension,
):

    local_file_path = os.path.join(
        test_file_directory_download,
        f"{file_name}_downloaded.{file_extension}",
    )

    download_file_from_model_version(
        model_version=test_model_version,
        neptune_attribute_path=f"model/{file_name}",
        local_file_path=local_file_path,
    )

    # clean up
    test_model_version.stop()
    os.remove(local_file_path)


@pytest.mark.order(2)
@pytest.mark.download
@pytest.mark.parametrize("test_model_version_mode", ["read-only"])
def download_directory_from_model_version_test(
    test_model_version,
    test_model_version_mode,
    test_file_directory_download,
    test_file_directory_upload,
):

    download_directory_from_model_version(
        model_version=test_model_version,
        local_directory_path=test_file_directory_download,
        neptune_attribute_path="model/test_file_directory",
    )
    # assemble expected, comparable ground truth download content
    # capture original upload dir content
    upload_directory_content = capture_directory_for_upload(
        local_directory_path=test_file_directory_upload, neptune_attribute_path=""
    )
    # retain the relative filepaths only for comparison purposes
    directory_content_expected = set(
        [
            os.path.relpath(item[0], test_file_directory_upload)
            for item in upload_directory_content
        ]
    )
    # assemble actual, comparable download content
    # capture the newly created downloaded directory content
    download_directory_content = capture_directory_for_upload(
        local_directory_path=test_file_directory_download,
        neptune_attribute_path="",
        exclude=[],
    )
    # retain the relative filepaths only for comparison purposes
    directory_content_actual = set(
        [
            os.path.relpath(item[0], test_file_directory_download)
            for item in download_directory_content
        ]
    )

    assert set(directory_content_actual) == set(directory_content_expected)

    # clean up
    test_model_version.stop()
    shutil.rmtree(test_file_directory_download)


@pytest.mark.order(2)
@pytest.mark.download
@pytest.mark.parametrize("test_model_version_mode", ["read-only"])
def download_config_from_model_version_test(
    test_model_version, test_model_version_mode, test_config_expected
):

    test_config_actual = download_config_from_model_version(
        model_version=test_model_version, neptune_attribute_path="test_config"
    )

    assert test_config_actual == test_config_expected

    test_model_version.stop()
