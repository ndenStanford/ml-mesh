# Standard Library
import json
import os
from datetime import datetime as dt
from pathlib import Path
from typing import Dict, Union

# 3rd party libraries
from neptune.metadata_containers.model_version import ModelVersion

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger()


def upload_file_to_model_version(
    model_version: ModelVersion,
    local_file_path: Union[str, Path],
    neptune_data_reference: str,
) -> None:
    """Utility function to upload a file to a specified model version on neptune ai."""

    if not os.path.exists(local_file_path):
        raise FileExistsError(f"Specified file {local_file_path} could not be located.")

    model_version[neptune_data_reference].upload(local_file_path)


def upload_directory_to_model_version(
    model_version: ModelVersion,
    local_directory_path: Union[str, Path],
    neptune_data_reference: str,
) -> None:
    """
    Utility function to upload a directory to a specified model version on neptune ai.
    For each file in the specified directory, the neptune_data_reference value will derived
    according to {neptune_data_reference}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

    Might want to add the option to exclude files and subdirectories from uploading in the future.

    """
    # catch invalid dir paths
    if not os.path.isdir(local_directory_path):
        raise FileExistsError(
            f"Specified path {local_directory_path} is not a valid directory."
        )
    # catch empty dirs
    files_considered_for_upload = os.listdir(local_directory_path)

    if not files_considered_for_upload:
        raise FileNotFoundError(
            f"Specified directory {local_directory_path} seems to be empty."
        )
    else:
        logger.debug(f"Uploading the following files: {files_considered_for_upload}")
    # nested subdirectories and files of any recursion depth should be supported
    for file_directory_path, _, file_names in os.walk(local_directory_path):
        for file_name in file_names:
            # get file path relative to specified local directory & replace OS separators with '/'s
            local_file_path = os.path.join(file_directory_path, file_name)
            file_neptune_data_reference = os.path.relpath(
                local_file_path, local_directory_path
            ).replace(os.sep, "/")
            # prepend file's neptune data reference with specified directory level neptune data
            # reference
            directory_file_neptune_data_reference = (
                f"{neptune_data_reference}/{file_neptune_data_reference}"
            )
            # upload file
            upload_file_to_model_version(
                model_version=model_version,
                local_file_path=local_file_path,
                neptune_data_reference=directory_file_neptune_data_reference,
            )

            logger.debug(
                f"Uploaded file {local_file_path} to neptune data reference",
                f"{directory_file_neptune_data_reference}",
            )


def upload_config_to_model_version(
    model_version: ModelVersion, config: Dict, neptune_data_reference: str
) -> None:
    """
    Utility function that allows uploading of python dictionaries as .json files directly using
    a local cache."""
    # sanity check neptune_data_reference for .json ending - otherwise file won't get displayed
    # as json file on neptune dashboard
    if not neptune_data_reference.endswith(".json"):
        neptune_data_reference_edited = f"{neptune_data_reference}.json"
        logger.warning(
            f"Editing config neptune data reference {neptune_data_reference} with"
            f'".json" file ending: {neptune_data_reference_edited}'
        )
        neptune_data_reference = neptune_data_reference_edited
    # temporarily save down config as json
    temp_time_stamp = dt.now().strftime("%Y_%m_%d__%H_%M_%s")
    temp_file_path = os.path.join(".", f"temp_neptune_config_{temp_time_stamp}.json")
    with open(temp_file_path, "w") as temp_config_file:
        json.dump(config, temp_config_file)

    upload_file_to_model_version(
        model_version=model_version,
        local_file_path=temp_file_path,
        neptune_data_reference=neptune_data_reference,
    )
    # remove temporary file
    os.remove(temp_file_path)
