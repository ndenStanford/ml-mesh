# Standard Library
import os
from pathlib import Path
from typing import Any, List, Tuple, Union

# 3rd party libraries
from neptune.attributes.atoms.file import File
from neptune.metadata_containers.model_version import ModelVersion

# Internal libraries
from onclusiveml.core.logging import get_default_logger


logger = get_default_logger(__name__, level=10)


def download_file_from_model_version(
    model_version: ModelVersion,
    neptune_data_reference: str,
    local_file_path: Union[str, Path],
) -> None:
    """Utility function to download a file from a specified model version on neptune ai.

    Args:
        model_version (ModelVersion): The registered neptune model version that this meta data
            should be attached to
        local_file_path (Union[str, Path]): The local file path the file should be downloaded to.
            Only supports local file systems.
        neptune_data_reference (str): The pseudo relative file path of the meta data object that
            should be downloaded.
    Raises:
        FileExistsError: If the specified `local_file_path` points to an existing file, this
            exception will be raised.
    """

    if os.path.exists(local_file_path):
        raise FileExistsError(f"Specified file {local_file_path} already exists.")

    model_version[neptune_data_reference].download(local_file_path)


def _extract_file_attributes(value: Any) -> Any:
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

    for v in value.values():

        if isinstance(v, dict):
            yield from _extract_file_attributes(v)
        elif isinstance(v, File):
            yield v
        else:
            continue


def _derive_and_filter_file_neptune_data_paths(
    file_attributes: List[File], neptune_reference_prefix: str
) -> List[Tuple[str, str]]:
    """Utility function that derives the full neptune model registry path for all File instances
    specified and deselected all those that don't start with the specified
    `neptune_reference_prefix`.

    Args:
        file_attributes (List[File]): A list of File instances as they appear in a ModelVersion's
            structure.
        neptune_reference_prefix (str): A string prefix that functions as a filter. Only those File
            instances in `file_attributes` whose neptune data reference starts with
            `neptune_reference_prefix` are retained.

    Returns:
        List[Tuple[str,str]]: A list of neptune data reference tuple, one with and one without the
            file extension, respectively.
    """ """"""

    filtered_neptune_data_paths = []

    for file_attribute in file_attributes:
        # construct neptune file reference and apply prefix filter
        neptune_data_file_reference = "/".join(file_attribute._path)

        if (
            neptune_reference_prefix != ""
            and not neptune_data_file_reference.startswith(neptune_reference_prefix)
        ):
            logger.debug(
                f"Neptune data path {neptune_data_file_reference} does not start with "
            )
            logger.debug(
                f"required neptune data prefix {neptune_reference_prefix}. Skipping..."
            )
            continue
        else:
            logger.debug(f"Neptune data path {neptune_data_file_reference} qualifies.")
        # if file attribute has the right neptune reference, append the extension for a full
        # file path-like string and add to instances to be returned
        neptune_data_file_path = (
            f"{neptune_data_file_reference}"  # .{file_attribute.fetch_extension()}'
        )

        filtered_neptune_data_paths.append(
            (neptune_data_file_reference, neptune_data_file_path)
        )

    return filtered_neptune_data_paths


def _convert_neptune_data_path_to_local_path(
    neptune_data_path: str,
    neptune_reference_prefix: str,
    local_directory_path: Union[str, Path],
    create_local_subdirs: bool = True,
) -> Union[str, Path]:
    """Utility function that converts a neptune file data reference to a valid, sensible local path,
    prefixed with the specified `local_directory_path` path.

    Args:
        neptune_data_paths (str): A list of neptune data references to be converted to
            equivalent local paths.
        neptune_reference_prefix (str): The neptune data reference prefix that all these paths have
            in common. Will essentially be replaced with the `local_directory_path`
        local_directory_path (Union[str, Path]): A path to a valid local directory.

    Returns:
        Union[str,Path]: The converted neptune data path - a valid local file path.
    """
    # remove any non-trivial neptune prefix from all paths
    if neptune_reference_prefix != "":
        logger.debug(
            f"Removing non-trivial neptune data prefix {neptune_reference_prefix}/ from"
        )
        logger.debug(f" neptune data path {neptune_data_path}")
        neptune_data_path = neptune_data_path.replace(
            f"{neptune_reference_prefix}/", ""
        )
    # convert to valid relative file path by inserting OS specific separators
    local_file_path = neptune_data_path.replace("/", os.sep)
    logger.debug(f"Created local file path {local_file_path} from neptune data path")
    logger.debug(f"{neptune_data_path}.")
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
    neptune_data_reference: str,
) -> List[Tuple[str, Union[Path, str]]]:
    """Utility function that gathers all File objects located under the specified
    `neptune_data_reference` of the specified model version instance, and assumes them to be the
    result of a previous upload_directory_to_model_version call. Reconstructs their respective
    attribute references and uses them to build a local file system file path prepended by the
    specified `local_directory` path.

    Returns a

    Args:
        model_version (ModelVersion): _description_
        local_directory_path (Union[str, Path]): _description_
        neptune_data_reference (str): _description_

    Returns:
        List[Tuple[str,str]]: A list of tuples containing the
        - attribute reference
        - local file path, prepended with the specified `local_directory_path`
        for each identified attribute sitting under the specified `neptune_data_reference`.
    """
    # traverse entire model_version structure dictionary and extract any and all File type attribute
    # leafs
    model_version_file_attributes = _extract_file_attributes(
        model_version.get_structure()
    )
    # derive the neptune data references with and without file extensions for relevant File
    # attributes only
    neptune_file_references_and_file_paths = _derive_and_filter_file_neptune_data_paths(
        file_attributes=model_version_file_attributes,
        neptune_reference_prefix=neptune_data_reference,
    )
    # convert the neptune file paths into valid local paths; retain the neptune file references
    neptune_file_references_and_local_file_paths = [
        (
            neptune_file_reference,
            _convert_neptune_data_path_to_local_path(
                neptune_file_data_path,
                neptune_reference_prefix=neptune_data_reference,
                local_directory_path=local_directory_path,
            ),
        )
        for (
            neptune_file_reference,
            neptune_file_data_path,
        ) in neptune_file_references_and_file_paths
    ]

    return neptune_file_references_and_local_file_paths


def download_directory_from_model_version(
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
        logger.info(
            f"Specified directory {local_directory_path} does not exist. Creating... "
        )
        os.makedirs(local_directory_path)
    # for all File attributes under the specified `neptune_data_reference`, retrieve:
    # - the neptune data reference of the File
    # - the equivalent local file path that the File should be downloaded to, considering the
    #    specified `local_directory_path`
    neptune_file_references_and_local_file_paths = capture_directory_for_download(
        model_version=model_version,
        local_directory_path=local_directory_path,
        neptune_data_reference=neptune_data_reference,
    )
    # apply the file level download function for all File instances retrieved
    for (
        neptune_file_reference,
        local_file_path,
    ) in neptune_file_references_and_local_file_paths:
        download_file_from_model_version(
            model_version=model_version,
            neptune_data_reference=neptune_file_reference,
            local_file_path=local_file_path,
        )

        logger.info(
            f"Downloaded file attribute referenced by {neptune_file_reference} to local path ",
        )
        logger.info(f"{local_file_path}.")
