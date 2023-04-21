# Standard Library
import os

# 3rd party libraries
import pytest

# Internal libraries
from onclusiveml.ml_tracking.download import (
    download_directory_from_model_version,
    download_file_from_model_version,
)


@pytest.mark.download
@pytest.mark.parametrize(
    "file_name,file_extension",
    [
        ("test_file_1", "json"),
        ("test_file_2", "txt"),
    ],
)
def download_file_from_model_version_test(
    test_model_version, test_file_directory_download, file_name, file_extension
):

    download_file_from_model_version(
        model_version=test_model_version,
        neptune_data_reference=f"model/{file_name}",
        local_file_path=os.path.join(
            test_file_directory_download,
            f"{file_name}_downloaded.{file_extension}",
        ),
    )


@pytest.mark.download
def download_directory_from_model_version_test(
    test_model_version, test_file_directory_download
):

    download_directory_from_model_version(
        model_version=test_model_version,
        local_directory_path=test_file_directory_download,
        neptune_data_reference="model/test_file_directory",
    )
