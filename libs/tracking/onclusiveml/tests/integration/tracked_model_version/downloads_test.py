# Standard Library
import os
import shutil

# 3rd party libraries
import pytest


@pytest.mark.order(2)
@pytest.mark.download
@pytest.mark.parametrize(
    "test_use_s3_backend",
    [
        False,
        True,
    ],
)
@pytest.mark.parametrize("test_model_version_mode", ["read-only"])
@pytest.mark.parametrize(
    "file_name,file_extension",
    [
        ("test_file_1", "json"),
        ("test_file_2", "txt"),
    ],
)
def test_download_file_from_model_version(
    test_model_version,
    test_use_s3_backend,
    test_model_version_mode,
    test_file_directory_download,
    file_name,
    file_extension,
):

    local_file_path = os.path.join(
        test_file_directory_download,
        f"{file_name}_downloaded.{file_extension}",
    )

    print(f"test_file_directory_download: {test_file_directory_download}")

    test_model_version.download_file_from_model_version(
        neptune_attribute_path=f"model/s3_{test_use_s3_backend}/{file_name}",
        local_file_path=local_file_path,
    )

    # clean up
    test_model_version.stop()
    shutil.rmtree(test_file_directory_download)


@pytest.mark.order(2)
@pytest.mark.download
@pytest.mark.parametrize(
    "test_use_s3_backend",
    [
        False,
        True,
    ],
)
@pytest.mark.parametrize("test_model_version_mode", ["read-only"])
def test_download_directory_from_model_version(
    test_model_version_mode,
    test_model_version,
    test_use_s3_backend,
    test_file_directory_download,
    test_file_directory_upload,
):

    test_model_version.download_directory_from_model_version(
        local_directory_path=test_file_directory_download,
        neptune_attribute_path=f"model/s3_{test_use_s3_backend}/test_file_directory",
    )
    # assemble expected, comparable ground truth download content
    # capture original upload dir content
    upload_directory_content = test_model_version.capture_directory_for_upload(
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
    download_directory_content = test_model_version.capture_directory_for_upload(
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
@pytest.mark.parametrize("test_model_version_mode", [(False, "read-only")])
def test_download_config_from_model_version(
    test_model_version,
    test_model_version_mode,
    test_config_expected,
):

    test_config_actual = test_model_version.download_config_from_model_version(
        neptune_attribute_path=f"s3_{False}/test_config",
    )

    test_model_version.stop()

    assert test_config_actual == test_config_expected


@pytest.mark.order(2)
@pytest.mark.download
def test_download_model_card_from_model_version(
    test_model_version, test_model_card_expected
):

    test_model_card_actual = test_model_version.download_config_from_model_version(
        neptune_attribute_path=f"s3_{False}/test_model_card",
    )

    test_model_version.stop()

    assert test_model_card_actual == test_model_card_expected
