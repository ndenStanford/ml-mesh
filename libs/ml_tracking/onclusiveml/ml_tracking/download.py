# Standard Library
import json
import os
from datetime import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

# 3rd party libraries
from neptune.attributes.atoms.file import File
from neptune.metadata_containers.model_version import ModelVersion

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=10)


def download_file_from_model_version(
    model_version: ModelVersion,
    neptune_attribute_path: str,
    local_file_path: Union[str, Path],
) -> None:
    """Utility function to download a file from a specified model version on neptune ai.

    Download counterpart to the `upload.upload_file_to_model_version` method.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_file_path (Union[str, Path]): The local file path the file should be downloaded to.
            Only supports local file systems.
        neptune_attribute_path (str): The pseudo relative file path of the meta data object that
            should be downloaded.
    Raises:
        FileExistsError: If the specified `local_file_path` points to an existing file, this
            exception will be raised.
    """

    if os.path.exists(local_file_path):
        raise FileExistsError(f"Specified file {local_file_path} already exists.")

    logger.debug(
        f"Downloading file {neptune_attribute_path} into local file {local_file_path}."
    )

    model_version[neptune_attribute_path].download(local_file_path)

    logger.debug(
        f"Downloaded file {neptune_attribute_path} into local file {local_file_path}."
    )


def _extract_file_attributes(value: Any) -> Union[File, Dict]:
    """Utility function to unravel a ModelVersion structure attribute dict and extract all the
    File type elements no matter how deeply nested.

    Args:
        value (Any): Since this is a recursive function, this can be one of the following:
            - a dictionary type in case of nested attributes
            - a File type attribute
            - some other non-File attribute supported by neptune

    Returns:
        Any: N/A

    Yields:
        Iterator[Any]: Either a File instance or a dictionary
    """ """"""

    for k, v in value.items():

        if isinstance(v, dict):
            logger.debug(
                f"Value of key {k} is type Dict. Adding recursion level for {v}."
            )
            yield from _extract_file_attributes(v)
        elif isinstance(v, File):
            logger.debug(f"Value of key {k} is File. Yielding {v}.")
            yield v
        else:
            logger.debug(f"Value of key {k} is of type {type(v)}. Skipping.")
            continue


def _derive_and_filter_neptune_attribute_paths(
    file_attributes: List[File], neptune_attribute_prefix: str
) -> List[str]:
    """Utility function that derives the full neptune model registry path for all File instances
    specified and deselected all those that don't start with the specified
    `neptune_attribute_prefix`.

    Args:
        file_attributes (List[File]): A list of File instances, roughly in depth first order as
            they appear in a ModelVersion's structure.
        neptune_attribute_prefix (str): A string prefix that functions as a filter. Only those File
            instances in `file_attributes` whose neptune data reference starts with
            `neptune_attribute_prefix` are retained.

    Returns:
        List[str]: A list of neptune attribute paths.
    """ """"""

    filtered_neptune_attribute_paths = []

    for file_attribute in file_attributes:
        # construct neptune file reference and apply prefix filter
        neptune_attribute_path = "/".join(file_attribute._path)

        if neptune_attribute_prefix != "" and not neptune_attribute_path.startswith(
            neptune_attribute_prefix
        ):
            logger.debug(
                f"Neptune data path {neptune_attribute_path} does not start with "
            )
            logger.debug(
                f"required neptune data prefix {neptune_attribute_prefix}. Skipping..."
            )
            continue
        else:
            logger.debug(f"Neptune data path {neptune_attribute_path} qualifies.")

        filtered_neptune_attribute_paths.append(neptune_attribute_path)

    return filtered_neptune_attribute_paths


def _convert_neptune_attribute_path_to_local_path(
    neptune_attribute_path: str,
    neptune_attribute_prefix: str,
    local_directory_path: Union[str, Path],
    create_local_subdirs: bool = True,
) -> Union[str, Path]:
    """Utility function that converts a neptune file data reference to a valid, sensible local path,
    prefixed with the specified `local_directory_path` path.

    Args:
        neptune_attribute_path (str): A neptune attribute path to be converted to
            equivalent local path.
        neptune_attribute_prefix (str): The neptune attribute prefix that all these paths have
            in common. Will essentially be replaced with the `local_directory_path`
        local_directory_path (Union[str, Path]): A path to a valid local directory.

    Returns:
        Union[str,Path]: The converted neptune data path - a valid local file path.
    """
    # remove any non-trivial neptune prefix from all paths
    if neptune_attribute_prefix != "":
        logger.debug(
            f"Removing non-trivial neptune data prefix {neptune_attribute_prefix}/ from"
        )
        logger.debug(f" neptune data path {neptune_attribute_path}")
        neptune_attribute_path = neptune_attribute_path.replace(
            f"{neptune_attribute_prefix}/", ""
        )
    # convert to valid relative file path by inserting OS specific separators
    local_file_path = neptune_attribute_path.replace("/", os.sep)
    logger.debug(f"Created local file path {local_file_path} from neptune data path")
    logger.debug(f"{neptune_attribute_path}.")
    # prepend local file path with specified directory location
    local_directory_file_path = os.path.join(local_directory_path, local_file_path)
    logger.debug(
        f"Created local directory file path {local_directory_file_path} from file path "
    )
    logger.debug(f"{local_file_path}.")

    if create_local_subdirs:
        local_subdirectory_path = os.path.join(
            *os.path.split(local_directory_file_path)[:-1]
        )

        if not os.path.isdir(local_subdirectory_path):
            os.makedirs(local_subdirectory_path)
            logger.debug(f"Created local subdirectory {local_subdirectory_path}.")

    return local_directory_file_path


def capture_directory_for_download(
    model_version: ModelVersion,
    local_directory_path: Union[str, Path],
    neptune_attribute_path: str,
) -> List[Tuple[str, Union[Path, str]]]:
    """Utility function that gathers all File objects located under the specified
    `neptune_attribute_path` of the specified model version instance, and assumes them to be the
    result of a previous upload_directory_to_model_version call. Reconstructs their respective
    attribute references and uses them to build a local file system file path prepended by the
    specified `local_directory` path.

    Returns a

    Args:
        model_version (ModelVersion): _description_
        local_directory_path (Union[str, Path]): _description_
        neptune_attribute_path (str): The attribute path prefix for the directory on neptune ai's
            model registry. The neptune attribute equivalent to the relative path to the local
            directory on disk. Must be specified.

    Returns:
        List[Tuple[str,str]]: A list of tuples containing the
        - attribute reference
        - local file path, prepended with the specified `local_directory_path`
        for each identified attribute sitting under the specified `neptune_attribute_path`.
    """
    # traverse entire model_version structure dictionary and extract any and all File type attribute
    # leafs
    model_version_file_attributes = list(
        _extract_file_attributes(model_version.get_structure())
    )
    # derive the neptune data references with and without file extensions for relevant File
    # attributes only
    neptune_attribute_paths = _derive_and_filter_neptune_attribute_paths(
        file_attributes=model_version_file_attributes,
        neptune_attribute_prefix=neptune_attribute_path,
    )
    # convert the neptune file paths into valid local paths; retain the neptune file references
    neptune_attribute_and_local_paths = [
        (
            neptune_attribute_path,
            _convert_neptune_attribute_path_to_local_path(
                neptune_attribute_path=neptune_attribute_path,
                neptune_attribute_prefix=neptune_attribute_path,
                local_directory_path=local_directory_path,
            ),
        )
        for neptune_attribute_path in neptune_attribute_paths
    ]

    return neptune_attribute_and_local_paths


def download_directory_from_model_version(
    model_version: ModelVersion,
    local_directory_path: Union[str, Path],
    neptune_attribute_path: str,
) -> None:
    """Utility function to upload an entire directory to a specified model version on neptune ai.
    For each file in the specified directory, the neptune_attribute_path value will derived
    according to {neptune_attribute_path}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

    Might want to add the option to exclude files and subdirectories from uploading in the future.

    Download counterpart to the `upload.upload_directory_to_model_version` method.

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
        logger.info(
            f"Specified directory {local_directory_path} does not exist. Creating... "
        )
        os.makedirs(local_directory_path)
    # for all File attributes under the specified `neptune_attribute_path`, retrieve:
    # - the neptune data reference of the File
    # - the equivalent local file path that the File should be downloaded to, considering the
    #    specified `local_directory_path`
    neptune_attribute_and_local_paths = capture_directory_for_download(
        model_version=model_version,
        local_directory_path=local_directory_path,
        neptune_attribute_path=neptune_attribute_path,
    )
    # apply the file level download function for all File instances retrieved
    for (
        neptune_attribute_path,
        local_file_path,
    ) in neptune_attribute_and_local_paths:
        download_file_from_model_version(
            model_version=model_version,
            neptune_attribute_path=neptune_attribute_path,
            local_file_path=local_file_path,
        )

        logger.info(
            f"Downloaded file attribute referenced by {neptune_attribute_path} to local path ",
        )
        logger.info(f"{local_file_path}.")


def download_config_from_model_version(
    model_version: ModelVersion, neptune_attribute_path: str
) -> Dict:
    """Utility function that fetches .json type File attributes from a specified neptune model
    version. Downloads the file into a temporary file on local disk and removes it once the object
    has been loaded into the python session.

    Download counterpart to the `upload.upload_config_to_model_version` method.

    Args:
        model_version (ModelVersion): The registered neptune model version that this config should
        be attached to
        config (Dict): The configuration dictionary that should be uploaded
        neptune_attribute_path (str): The pseudo relative file path of the meta data object that
            will be created. Relative w.r.t to the model version as pseudo root dir.
    """

    temp_file_name = f"{dt.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}.json"

    download_file_from_model_version(
        model_version=model_version,
        neptune_attribute_path=neptune_attribute_path,
        local_file_path=temp_file_name,
    )

    with open(temp_file_name, "r") as temp_file:
        config_file = json.load(temp_file)

    logger.debug(f"Removing temp config file {temp_file_name}")

    os.remove(temp_file_name)

    logger.debug(f"Removed temp config file {temp_file_name}")

    return config_file
