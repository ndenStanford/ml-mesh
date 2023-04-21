# Standard Library
import os
from pathlib import Path
from typing import List, Tuple, Union

# 3rd party libraries
from neptune.metadata_containers.model_version import ModelVersion

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__)


def upload_file_to_model_version(
    model_version: ModelVersion,
    local_file_path: Union[str, Path],
    neptune_data_reference: str,
) -> None:
    """Utility function to upload a file to a specified model version on neptune ai.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_file_path (Union[str, Path]): The local file path to the file that should be uploaded.
            Only supports local file systems.
        neptune_data_reference (str): The pseudo relative file path of the meta data object that
            will be created. Relative w.r.t to the model version as pseudo root dir.

    Raises:
        FileExistsError: If the specified `local_file_path` does not point to a valid file, this
            exception will be raised.
    """

    if not os.path.exists(local_file_path):
        raise FileExistsError(f"Specified file {local_file_path} could not be located.")

    model_version[neptune_data_reference].upload(local_file_path)


def capture_directory_for_upload(
    local_directory_path: Union[str, Path], neptune_data_reference: str
) -> List[Tuple[str, str]]:
    """Utility function that scans a specified directory on local disk, captures all files and
    transforms their respective relative file paths into neptune attribute references.

    Args:
        local_directory_path (Union[str, Path]): _description_

    Returns:
        List[Tuple[str, str]]: A list of tuples:
        - the file paths as well as
        - the attribute references, prepended with the specified directory path after it has been
            converted into a forward slash separated attribute reference prefix.
    """

    local_paths_and_attribute_references: List[Tuple[str, str]] = []

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
            if neptune_data_reference:
                directory_file_neptune_data_reference = (
                    f"{neptune_data_reference}/{file_neptune_data_reference}"
                )
            else:
                directory_file_neptune_data_reference = file_neptune_data_reference

            local_paths_and_attribute_references.append(
                (local_file_path, directory_file_neptune_data_reference)
            )

    return local_paths_and_attribute_references


def upload_directory_to_model_version(
    model_version: ModelVersion,
    local_directory_path: Union[str, Path],
    neptune_data_reference: str,
) -> None:
    """Utility function to upload an entire directory to a specified model version on neptune ai.
    For each file in the specified directory, the neptune_data_reference value will derived
    according to {neptune_data_reference}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

    Might want to add the option to exclude files and subdirectories from uploading in the future.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_directory_path (Union[str, Path]): The local directory path to the directory whose
            contents should be uploaded. Only supports local file systems.
        neptune_data_reference (str): The prefix to each individual file's neptune data reference
            pseudo path (see description)

    Raises:
        FileExistsError: If the specified `local_directory_path` does not point to a valid
            directory, this exception will be raised.

        FileNotFoundError: If the specified `local_directory_path` points to a valid directory,
            this exception will be raised.
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

    local_paths_and_attribute_references = capture_directory_for_upload(
        local_directory_path, neptune_data_reference
    )

    for (
        local_file_path,
        directory_file_neptune_data_reference,
    ) in local_paths_and_attribute_references:
        # upload file
        upload_file_to_model_version(
            model_version=model_version,
            local_file_path=local_file_path,
            neptune_data_reference=directory_file_neptune_data_reference,
        )

        logger.debug(f"Uploaded file {local_file_path} to neptune data reference")
        logger.debug(f"{directory_file_neptune_data_reference}")
