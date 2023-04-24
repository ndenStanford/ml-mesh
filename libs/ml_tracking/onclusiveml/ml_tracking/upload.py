# Standard Library
import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Union

# 3rd party libraries
from neptune.metadata_containers.model_version import ModelVersion
from neptune.types import File

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__)


def upload_file_to_model_version(
    model_version: ModelVersion,
    neptune_attribute_path: str,
    local_file_path: Union[str, Path] = "",
    file_object: File = None,
) -> None:
    """Utility function to upload a file to a specified model version on neptune ai.

    Upload counterpart to the `download.download_file_from_model_version` method.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_file_path (Union[str, Path]): The local file path to the file that should be uploaded.
            Only supports local file systems.
        neptune_attribute_path (str): The pseudo relative file path of the meta data object that
            will be created. Relative w.r.t to the model version as pseudo root dir.

    Raises:
        FileExistsError: If the specified `local_file_path` does not point to a valid file, this
            exception will be raised.
    """

    if not local_file_path and not file_object:
        raise ValueError(
            "At least one of `local_file_path` or `file_object` must be provided."
        )

    if local_file_path:
        if not os.path.exists(local_file_path):
            raise FileExistsError(
                f"Specified file {local_file_path} could not be located."
            )
        else:
            file_object = File.from_path(local_file_path)

    logger.debug(
        f"Uploading file {local_file_path} into attribute {neptune_attribute_path}."
    )

    model_version[neptune_attribute_path].upload(file_object)

    logger.debug(
        f"Uploaded file {local_file_path} into attribute {neptune_attribute_path}."
    )


def capture_directory_for_upload(
    local_directory_path: Union[str, Path], neptune_attribute_path: str
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
            file_neptune_attribute_path = os.path.relpath(
                local_file_path, local_directory_path
            ).replace(os.sep, "/")
            # prepend file's neptune data reference with specified directory level neptune data
            # reference
            if neptune_attribute_path:
                directory_file_neptune_attribute_path = (
                    f"{neptune_attribute_path}/{file_neptune_attribute_path}"
                )
            else:
                directory_file_neptune_attribute_path = file_neptune_attribute_path

            local_paths_and_attribute_references.append(
                (local_file_path, directory_file_neptune_attribute_path)
            )

    return local_paths_and_attribute_references


def upload_directory_to_model_version(
    model_version: ModelVersion,
    local_directory_path: Union[str, Path],
    neptune_attribute_path: str,
) -> None:
    """Utility function to upload an entire directory to a specified model version on neptune ai.
    For each file in the specified directory, the neptune_attribute_path value will derived
    according to {neptune_attribute_path}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

    Might want to add the option to exclude files and subdirectories from uploading in the future.

    Upload counterpart to the `download.download_directory_from_model_version` method.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_directory_path (Union[str, Path]): The local directory path to the directory whose
            contents should be uploaded. Only supports local file systems.
        neptune_attribute_path (str): The prefix to each individual file's neptune data reference
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
        local_directory_path, neptune_attribute_path
    )

    for (
        local_file_path,
        directory_file_neptune_attribute_path,
    ) in local_paths_and_attribute_references:
        # upload file
        upload_file_to_model_version(
            model_version=model_version,
            local_file_path=local_file_path,
            neptune_attribute_path=directory_file_neptune_attribute_path,
        )

        logger.debug(f"Uploaded file {local_file_path} to neptune data reference")
        logger.debug(f"{directory_file_neptune_attribute_path}")


def upload_config_to_model_version(
    model_version: ModelVersion, config: Dict, neptune_attribute_path: str
) -> None:
    """Utility function that uploads Dict types as .json objects directly to neptune's model version
    registry without having to go via local files or caches.

    Upload counterpart to the `download.download_config_from_model_version` method.

    Args:
        model_version (ModelVersion): The registered neptune model version that this config should
        be attached to
        config (Dict): The configuration dictionary that should be uploaded
        neptune_attribute_path (str): The pseudo relative file path of the meta data object that
            will be created. Relative w.r.t to the model version as pseudo root dir.
    """

    config_json = json.dumps(config, indent=4)

    logger.debug(f"JSON of config file: {config_json}")

    config_file = File.from_content(content=config_json, extension="json")

    upload_file_to_model_version(
        model_version=model_version,
        neptune_attribute_path=neptune_attribute_path,
        file_object=config_file,
    )

    return
