"""Model version."""

# Standard Library
import json
import logging
import os
from datetime import datetime as dt
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple, Union

# 3rd party libraries
import boto3
from neptune import ModelVersion
from neptune.attributes.atoms.artifact import Artifact as ArtifactAttributeType
from neptune.attributes.atoms.file import File as FileAttributeType
from neptune.exceptions import TypeDoesNotSupportAttributeException
from neptune.types import File

# Internal libraries
from onclusiveml.tracking.settings import TrackingBackendSettings


logger = logging.getLogger(__name__)


class TrackedModelVersion(ModelVersion):
    """Tracked model version."""

    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ):
        """Constructor for customized ModelVersion based object class.

        Args:
            s3_backend (str, optional): Bucket name. Defaults to ''.
        """
        super().__init__(*args, **kwargs)
        # configure s3 storage backend
        self.s3_storage_backend_config = TrackingBackendSettings()

    @property
    def s3_client(self) -> Any:
        """S3 bucket client instance getter."""
        return boto3.resource("s3").Bucket(self.s3_storage_backend_config.bucket_name)

    def derive_model_version_s3_prefix(self, s3_prefix: str = "") -> str:
        """Helper function that assembles the S3 storage prefix for the current model version.

        Uses the pattern:

        ({s3_prefix}/){workspace}/{project}/{model}-{model_version}, e.g.

        model_registry/onclusive/keywords/KEYWORDS-TRAINED-4

        Args:
            s3_prefix (str, optional): A valid S3 prefix, if users want to specify a bucket
                "subdirectory" for a given model version. Defaults to ''.

        Returns:
            str: The model version level S3 prefix. Will be used to prepend any and all file
                attribute S3 prefixes associated to this model version.
        """
        model_version_s3_prefix = (
            f"{self._workspace}/{self._project_name}/{self._model}/{self._sys_id}"
        )

        if s3_prefix:
            model_version_s3_prefix = f"{s3_prefix}/{model_version_s3_prefix}"

        return model_version_s3_prefix

    # --- Upload utilities
    def upload_file_to_model_version(
        self,
        neptune_attribute_path: str,
        local_file_path: Union[str, Path] = "",
        file_object: File = None,
        **kwargs: Any,
    ) -> None:
        """Utility function to upload a file to a specified model version on neptune ai.

        Upload counterpart to the `download.download_file_from_model_version` method.

        Args:
            neptune_attribute_path (str): The pseudo relative file path of the meta data object that
                will be created. Relative w.r.t to the model version as pseudo root dir.
            local_file_path (Union[str, Path]): The local file path to the file that should be
                uploaded. Only supports local file systems. Must point to a valid file.
            file_object (File): A neptune type file object. Can be passed instead of the
                `local_file_path` argument. At least one of `file_object` and `local_file_path`
                must be specified.
            **kwargs (Any): The upload_file_to_model_version kwargs. Specify `use_s3=True` here to
                make use of the configured S3 storage backend when uploading the config dictionary

        Raises:
            FileExistsError: If the specified `local_file_path` does not point to a valid file, this
                exception will be raised.
        """
        # if the use of s3 storage is not specified at the file upload level, fall back on
        # `s3_storage_backend_config` parameter
        use_s3 = kwargs.get("use_s3", self.s3_storage_backend_config.use_s3_backend)
        # if a file object is specified, enforce neptune ai storage backend as uploading configs
        # directly is not yet supported by S3 backend
        # if no file object is specified, ensure a valid local file path is specified and create a
        # neptune file object from it
        if file_object is not None:

            logger.info("File object specified. Enforcing neptune storage backend.")
            use_s3 = False

        elif file_object is None and local_file_path:

            logger.debug(
                "File object not specified, but file path specified. Attempting to create "
                f"file object from file path {local_file_path}."
            )

            if not os.path.exists(local_file_path):
                raise FileExistsError(
                    f"Specified file {local_file_path} could not be located."
                )
            else:
                file_object = File.from_path(local_file_path)
                logger.debug(f"Created file object from file path {local_file_path}.")

        elif file_object is None and not local_file_path:
            raise ValueError(
                "At least one of `local_file_path` or `file_object` must be provided."
            )
        else:
            raise NotImplementedError(
                f"Unforeseen specification: File object {file_object}."
                f"File path {local_file_path}."
            )
        # upload the file:
        # - if storage backend is configured to neptune ai servers, upload the file object
        # - if storage backend is configured to internal S3:
        #     - upload the file from the local_file_path spec using boto3, then
        #     - use neptune's built-in track_files method to create meta data reference to S3
        #       objects and the model version entry on the neptune model registry
        #
        # NOTE: Currently doesnt support the upload_config method, as neptune file objects are not
        # implementing a read method required for boto3's upload_fileobj method
        if not use_s3:
            self[neptune_attribute_path].upload(file_object)
            logger.debug(
                f"Uploaded file object {file_object} into attribute {neptune_attribute_path}."
            )
        else:
            _ = self.upload_tracked_file_to_s3(
                neptune_attribute_path=neptune_attribute_path,
                local_file_path=local_file_path,
            )

    def upload_tracked_file_to_s3(
        self,
        neptune_attribute_path: str,
        local_file_path: Union[str, Path] = "",
    ) -> str:
        """Uploads files to S3.

        Utility to
            - generate an S3 bucket client for the configured storage backend 3 bucket
            - upload the designated file from local to the model version and neptune attribute path
                specific S3 location
            - track the uploaded file via neptune's track_files method, thus adding it to the
                TrackedModelVersion's meta data for the python object instance, and subsequently
                also to the resulting model registry entry

        Args:
            neptune_attribute_path (str): _description_
            local_file_path (Union[str, Path], optional): _description_. Defaults to "".

        Returns:
            str: The full S3 uri of the uploaded file
        """
        s3_bucket = self.s3_storage_backend_config.bucket_name
        s3_bucket_root = self.s3_storage_backend_config.s3_backend_root

        # assemble full s3 uri for file
        s3_model_version_prefix = self.derive_model_version_s3_prefix(s3_bucket_root)
        s3_file_prefix = f"{s3_model_version_prefix}/{neptune_attribute_path}"
        s3_file_uri = f"s3://{s3_bucket}/{s3_file_prefix}"

        logger.debug(
            f"Uploading file {local_file_path} into S3 bucket {s3_bucket}: "
            f"{s3_file_prefix}."
        )

        self.s3_client.upload_file(local_file_path, s3_file_prefix)

        logger.debug(
            f"Uploaded file {local_file_path} into S3 bucket {s3_bucket}: "
            f"{s3_file_prefix}."
        )

        self[neptune_attribute_path].track_files(s3_file_uri)

        logger.debug(
            f"Tracked file in S3 bucket {s3_bucket}: {s3_file_prefix} under attribute path "
            f"{neptune_attribute_path}"
        )

        return s3_file_uri

    @staticmethod
    def capture_directory_for_upload(
        local_directory_path: Union[str, Path],
        neptune_attribute_path: str,
        exclude: List[str] = ["__", "."],
    ) -> List[Tuple[str, str]]:
        """Registers directory files to be uploaded.

        Utility function that scans a specified directory on local disk, captures all files and
        transforms their respective relative file paths into neptune attribute references.

        Args:
            local_directory_path (Union[str, Path]): The path to the local directory whose content
                needs to be captured and prepped for uploading to neptune
            neptune_attribute_path (str): The attribute path prefix that should be applied to all
                files captured. The neptune attribute path equivalent to the files' local file
                paths' local directory prefix.
            exclude (List[str], optional): Prefixes for files and directories to be excluded.
                Defaults to ('__','.').

        Returns:
            List[Tuple[str, str]]: A list of tuples:
            - the file paths as well as
            - the attribute references, prepended with the specified directory path after it has
                been converted into a forward slash separated attribute reference prefix.
        """
        local_paths_and_attribute_references: List[Tuple[str, str]] = []
        # nested subdirectories and files of any recursion depth should be supported
        for file_directory_path, subdirs, file_names in os.walk(
            local_directory_path, topdown=True
        ):
            # reduce effort by dynamically removing irrelevant files & dirs, as per
            # https://stackoverflow.com/questions/13454164/os-walk-without-hidden-folders
            if exclude:
                exclude_tuple = tuple(exclude)
                file_names = [
                    filename
                    for filename in file_names
                    if not filename.startswith(exclude_tuple)
                ]
                subdirs[:] = [
                    subdir for subdir in subdirs if not subdir.startswith(exclude_tuple)
                ]

            for file_name in file_names:
                # get file path relative to specified local directory & replace OS separators with
                # '/'s
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
        self,
        local_directory_path: Union[str, Path],
        neptune_attribute_path: str,
        exclude: List[str] = ["__", "."],
        **kwargs: Any,
    ) -> None:
        """Uploads entire directory to model registry.

        Utility function to upload an entire directory to a specified model version on neptune
        ai. For each file in the specified directory, the neptune_attribute_path value will derived
        according to
            {neptune_attribute_path}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

        Upload counterpart to the `download.download_directory_from_model_version` method.

        Args:
            local_directory_path (Union[str, Path]): The local directory path to the directory whose
                contents should be uploaded. Only supports local file systems.
            neptune_attribute_path (str): The prefix to each individual file's neptune data
                reference pseudo path (see description)
            exclude (List[str], optional): Prefixes for files and directories to be excluded.
                Defaults to ['__','.'].
            **kwargs (Any): The upload_file_to_model_version kwargs. Specify `use_s3=True` here to
                make use of the configured S3 storage backend when uploading the directory

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
            logger.debug(
                f"Uploading the following files: {files_considered_for_upload}"
            )

        local_paths_and_attribute_references = self.capture_directory_for_upload(
            local_directory_path, neptune_attribute_path, exclude
        )

        for (
            local_file_path,
            directory_file_neptune_attribute_path,
        ) in local_paths_and_attribute_references:
            # upload file
            self.upload_file_to_model_version(
                local_file_path=local_file_path,
                neptune_attribute_path=directory_file_neptune_attribute_path,
                **kwargs,
            )

            logger.debug(f"Uploaded file {local_file_path} to neptune data reference")
            logger.debug(f"{directory_file_neptune_attribute_path}")

    def upload_config_to_model_version(
        self, config: Dict, neptune_attribute_path: str, **kwargs: Any
    ) -> None:
        """Uploads configuration to model registry.

        Utility function that uploads Dict types as .json objects directly to neptune's model
        version registry without having to go via local files or caches.

        Upload counterpart to the `download.download_config_from_model_version` method.

        Args:
            config (Dict): The configuration dictionary that should be uploaded
            neptune_attribute_path (str): The pseudo relative file path of the meta data object that
                will be created. Relative w.r.t to the model version as pseudo root dir.
            **kwargs (Any): The upload_file_to_model_version kwargs. Specify `use_s3=True` here to
                make use of the configured S3 storage backend when uploading the config dictionary
        """
        config_json = json.dumps(config, indent=4)

        logger.debug(f"JSON of config file: {config_json}")

        config_file = File.from_content(content=config_json, extension="json")

        self.upload_file_to_model_version(
            neptune_attribute_path=neptune_attribute_path,
            file_object=config_file,
            **kwargs,
        )

        return

    # --- Download utilities
    def download_file_from_model_version(
        self,
        neptune_attribute_path: str,
        local_file_path: Union[str, Path],
    ) -> None:
        """Utility function to download a file from a specified model version on neptune ai.

        Download counterpart to the `upload.upload_file_to_model_version` method.

        Args:
            local_file_path (Union[str, Path]): The local file path the file should be downloaded
                to. Only supports local file systems.
            neptune_attribute_path (str): The pseudo relative file path of the meta data object that
                should be downloaded.

        Raises:
            FileExistsError: If the specified `local_file_path` points to an existing file, this
                exception will be raised.
        """
        if os.path.exists(local_file_path):
            logger.info(
                f"Local file {local_file_path} already exists, and will be removed."
            )
            os.remove(local_file_path)

        logger.debug(
            f"Downloading File attribute {neptune_attribute_path} into local file "
            f"{local_file_path}.",
        )

        neptune_attribute = self[neptune_attribute_path]

        if self.is_likely_s3_backed_file(neptune_attribute):
            self.download_tracked_file_from_s3(
                neptune_attribute_path=neptune_attribute_path,
                local_file_path=local_file_path,
            )
        else:
            neptune_attribute.download(local_file_path)

        logger.debug(
            f"Downloaded File attribute {neptune_attribute_path} into local file {local_file_path}."
        )

    @staticmethod
    def is_likely_s3_backed_file(
        neptune_attribute: Union[ArtifactAttributeType, FileAttributeType, Any]
    ) -> bool:
        """Utility to identiy neptune attributes that are most likely backed by S3 storage.

        Because slightly different download behaviour of the two different attribute file types
            - neptune.attributes.atoms.file.File
                - will save attribute data in specified `destination` argument
            - neptune.attributes.atoms.artifact.Artifact
                - will create a directory in the specified `destination` argument, then save the
                    file using stored meta data to re-create the correct filename

        It is necessary to disambiguate these to ensure consistent download behaviour at the
        `download_file_from_model_version` method level.

        Args:
            neptune_attribute (_type_): The neptune attribute object whose backend storage type
                we are trying to infer

        Returns:
            bool: Whether we are most likely dealing with an attribute whose data is store on S3.
        """
        if not hasattr(neptune_attribute, "fetch_files_list"):
            return False
        else:
            try:
                neptune_artifact = neptune_attribute.fetch_files_list()[0]

                if neptune_artifact.metadata["location"].startswith("s3://"):
                    return True
                else:
                    return False

            except TypeDoesNotSupportAttributeException as not_implemented_error:
                logger.debug(
                    f"The attribute {neptune_attribute} does not support the "
                    f"fetch_files_list method: {not_implemented_error}."
                )
                return False

    def download_tracked_file_from_s3(
        self,
        neptune_attribute_path: str,
        local_file_path: Union[str, Path] = "",
    ) -> None:
        """Download utilities.

        Executres the following:
            - generate an S3 bucket client for the configured storage backend 3 bucket
            - download the designated file from s3 - by digging into the neptune Artifact object's
                metadata to obtain the S3 uri - to local disk

        Note that this assumes the underlying neptune artiact to only have one file, e.g. the result
        of calling `upload_tracked_file_to_s3`.

        Args:
            neptune_attribute_path (str): _description_
            local_file_path (Union[str, Path], optional): _description_. Defaults to "".

        Returns:
            None
        """
        s3_bucket = self.s3_storage_backend_config.bucket_name
        # extract the underlying s3 file's prefix as required by boto3's download_file method
        neptune_attribute = self[neptune_attribute_path]
        neptune_artifact = neptune_attribute.fetch_files_list()[0]
        tracked_file_s3_uri = neptune_artifact.metadata["location"]
        tracked_file_s3_prefix = tracked_file_s3_uri.replace(f"s3://{s3_bucket}/", "")

        logger.info(
            f"Downloading file {tracked_file_s3_uri} to local path {local_file_path}"
        )

        self.s3_client.download_file(tracked_file_s3_prefix, local_file_path)

        logger.info(
            f"Downloaded file {tracked_file_s3_uri} to local path {local_file_path}"
        )

    @classmethod
    def _extract_data_attributes(cls, value: Any) -> Iterator[Any]:
        """Utility function to unravel a ModelVersion structure attribute dict.

        Args:
            value (Any): Since this is a recursive function, this can be one of the following:
                - a dictionary type in case of nested attributes
                - a File type attribute
                - some other non-File attribute supported by neptune

        Yields:
            Iterator[Any]: Either a File instance or a dictionary
        """
        for k, v in value.items():

            if isinstance(v, dict):
                logger.debug(
                    f"Value of key {k} is type Dict. Adding recursion level for {v}."
                )
                yield from cls._extract_data_attributes(v)
            elif isinstance(v, (FileAttributeType, ArtifactAttributeType)):
                logger.debug(f"Value of key {k} is File. Yielding {v}.")
                yield v
            else:
                logger.debug(f"Value of key {k} is of type {type(v)}. Skipping.")
                continue

    @staticmethod
    def _derive_and_filter_neptune_attribute_paths(
        file_attributes: List[File], neptune_attribute_prefix: str
    ) -> List[str]:
        """Utility function that derives the full neptune model registry path.

        Args:
            file_attributes (List[File]): A list of File instances, roughly in depth first order as
                they appear in a ModelVersion's structure.
            neptune_attribute_prefix (str): A string prefix that functions as a filter. Only those
                File instances in `file_attributes` whose neptune data reference starts with
                `neptune_attribute_prefix` are retained.

        Returns:
            List[str]: A list of neptune attribute paths.
        """
        filtered_neptune_attribute_paths = []

        for file_attribute in file_attributes:
            # construct neptune file reference and apply prefix filter
            neptune_attribute_path = "/".join(file_attribute._path)

            if (
                neptune_attribute_prefix != ""
                and not neptune_attribute_path.startswith(  # noqa: W503
                    neptune_attribute_prefix
                )
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

    @staticmethod
    def _convert_neptune_attribute_path_to_local_path(
        neptune_attribute_path: str,
        neptune_attribute_prefix: str,
        local_directory_path: Union[str, Path],
        create_local_subdirs: bool = True,
    ) -> Union[str, Path]:
        """Utility function that converts a neptune file data reference to a local path.

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

            neptune_attribute_path = neptune_attribute_path[
                len(neptune_attribute_prefix) + 1 :  # noqa: E203
            ]
        # convert to valid relative file path by inserting OS specific separators
        local_file_path = neptune_attribute_path.replace("/", os.sep)
        logger.debug(
            f"Created local file path {local_file_path} from neptune data path"
        )
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
        self,
        local_directory_path: Union[str, Path],
        neptune_attribute_path: str,
    ) -> List[Tuple[str, Union[Path, str]]]:
        """Intenvories directory to be downloaded.

        Utility function that gathers all File objects located under the specified
        `neptune_attribute_path` of the specified model version instance, and assumes them to be the
        result of a previous upload_directory_to_model_version call. Reconstructs their respective
        attribute references and uses them to build a local file system file path prepended by the
        specified `local_directory` path.

        Args:
            local_directory_path (Union[str, Path]): _description_
            neptune_attribute_path (str): The attribute path prefix for the directory on neptune
                ai's model registry. The neptune attribute equivalent to the relative path to the
                local directory on disk. Must be specified.

        Returns:
            List[Tuple[str,str]]: A list of tuples containing the
            - attribute reference
            - local file path, prepended with the specified `local_directory_path`
            for each identified attribute sitting under the specified `neptune_attribute_path`.
        """
        # traverse entire model_version structure dictionary and extract any and all File type
        # attribute leafs
        model_version_file_attributes = list(
            self._extract_data_attributes(self.get_structure())
        )
        # derive the neptune data references with and without file extensions for relevant File
        # attributes only
        neptune_attribute_paths = self._derive_and_filter_neptune_attribute_paths(
            file_attributes=model_version_file_attributes,
            neptune_attribute_prefix=neptune_attribute_path,
        )
        # convert the neptune file paths into valid local paths; retain the neptune file references
        neptune_attribute_and_local_paths = [
            (
                neptune_attribute_path_i,
                self._convert_neptune_attribute_path_to_local_path(
                    neptune_attribute_path=neptune_attribute_path_i,
                    neptune_attribute_prefix=neptune_attribute_path,
                    local_directory_path=local_directory_path,
                ),
            )
            for neptune_attribute_path_i in neptune_attribute_paths
        ]

        return neptune_attribute_and_local_paths

    def download_directory_from_model_version(
        self,
        local_directory_path: Union[str, Path],
        neptune_attribute_path: str,
    ) -> None:
        """Utility function to upload an entire directory to a specified model version on neptuneai.

        For each file in the specified directory, the neptune_attribute_path value will
        be derived according to:
                {neptune_attribute_path}/{arbitrary}/{levels}/{of}/{subdirectories}/{file_name}.

        Might want to add the option to exclude files and subdirectories from uploading in the
        future.

        Download counterpart to the `upload.upload_directory_to_model_version` method.

        Args:
            local_directory_path (Union[str, Path]): The local directory path to the directory whose
                contents should be uploaded. Only supports local file systems.
            neptune_attribute_path (str): The prefix to each individual file's neptune data
                reference pseudo path (see description)

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
        neptune_attribute_and_local_paths = self.capture_directory_for_download(
            local_directory_path=local_directory_path,
            neptune_attribute_path=neptune_attribute_path,
        )
        # apply the file level download function for all File instances retrieved
        for (
            neptune_attribute_path_i,
            local_file_path_i,
        ) in neptune_attribute_and_local_paths:
            self.download_file_from_model_version(
                neptune_attribute_path=neptune_attribute_path_i,
                local_file_path=local_file_path_i,
            )

    def download_config_from_model_version(self, neptune_attribute_path: str) -> Dict:
        """Utility function that fetches .json type File attributes from a specified neptune model version.

        Downloads the file into a temporary file on local disk and removes it once the object has
        been loaded into the python session.

        Download counterpart to the `upload.upload_config_to_model_version` method.

        Args:
            config (Dict): The configuration dictionary that should be uploaded
            neptune_attribute_path (str): The pseudo relative file path of the meta data object that
                will be created. Relative w.r.t to the model version as pseudo root dir.
        """
        temp_file_name = f"{dt.now().strftime('%Y-%m-%d_%H-%M-%S.%f')}.json"

        self.download_file_from_model_version(
            neptune_attribute_path=neptune_attribute_path,
            local_file_path=temp_file_name,
        )

        with open(temp_file_name, "r") as temp_file:
            config_file = json.load(temp_file)

        logger.debug(f"Removing temp config file {temp_file_name}")

        os.remove(temp_file_name)

        logger.debug(f"Removed temp config file {temp_file_name}")

        return config_file
