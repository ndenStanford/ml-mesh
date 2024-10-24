"""Download compiled model."""

# Standard Library``

# Standard Library
import os

# 3rd party libraries
import boto3

# Internal libraries
from onclusiveml.core.base import OnclusiveBaseSettings
from onclusiveml.core.base.pydantic import cast
from onclusiveml.core.logging import (
    OnclusiveLogSettings,
    get_default_logger,
    init_logging,
)
from onclusiveml.tracking import TrackedModelVersion

# Source
from src.settings import get_settings


settings = get_settings()


def download_model(settings: OnclusiveBaseSettings) -> None:
    """Download compiled model."""
    logger = get_default_logger(
        name=__name__, fmt_level=settings.fmt_level, level=settings.level
    )
    # model registry reference to the desired (compiled) model version
    # initialize client for specific model version
    session = boto3.Session()
    s3 = session.client("s3")
    try:
        current_region = session.region_name
        # Print the current AWS region
        print(f"Current AWS region: {current_region}")
        # Create an S3 client
        # List all S3 buckets
        response = s3.list_buckets()
        # Print bucket names
        print("Available S3 buckets:")
        for bucket in response["Buckets"]:
            print(f"- {bucket['Name']}")
    except Exception as e:
        print("=======================error", e)

    try:
        bucket_name = "onclusive-model-store-prod"
        folders = [
            "neptune-ai-model-registry",
            "onclusive",
            "visitor-estimation",
            "VE-TRAINED",
            "VE-TRAINED-159",
            "model",
            "model_artifacts",
        ]

        def list_s3_contents(bucket, prefix):
            result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
            if "CommonPrefixes" in result:
                return [common_prefix["Prefix"] for common_prefix in result["CommonPrefixes"]]
            elif "Contents" in result:
                return [content["Key"] for content in result["Contents"]]
            else:
                return []

        def check_s3_folder_exists(bucket, prefix):
            result = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, Delimiter="/")
            return "CommonPrefixes" in result

        current_prefix = ""
        for folder in folders:
            current_prefix = f"{current_prefix}{folder}/"
            if check_s3_folder_exists(bucket_name, current_prefix):
                print(f"Folder {current_prefix} exists in S3.")
            else:
                print(f"Folder {current_prefix} does not exist in S3.")
                
                # Print the contents of the previous folder
                previous_prefix = "/".join(current_prefix.split("/")[:-2]) + "/"
                contents = list_s3_contents(bucket_name, previous_prefix)
                print(f"Contents of the previous folder ({previous_prefix}):", contents)
                print('>>>>', s3.list_objects_v2(Bucket=bucket, Prefix=previous_prefix, Delimiter="/"))
                for content in contents:
                    print(f" - {content}")
                break
        else:
            # Finally, check if the file exists
            full_file_key = f"{current_prefix}relevancemap.pkl"
            try:
                s3.head_object(Bucket=bucket_name, Key=full_file_key)
                print(f"File {full_file_key} exists in S3.")
            except s3.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "404":
                    print(f"File {full_file_key} does not exist in S3.")
                else:
                    raise

    except Exception as e:
        print(">>>>>>>>>>>>>>>>>>>error", e)

    mv = TrackedModelVersion(
        with_id=settings.with_id,
        mode=settings.mode,
        api_token=settings.api_token.get_secret_value(),
        project=settings.project,
    )

    if not os.path.isdir(settings.model_directory):
        # if the target dir does not exist, download all model artifacts for the model version to
        # local
        logger.debug(f"settings.model_directory: {settings.model_directory}")
        mv.download_directory_from_model_version(
            local_directory_path=settings.model_directory,
            neptune_attribute_path="model",
        )
    elif not os.listdir(settings.model_directory):
        # if the target dir does exist but is empty, download all model artifacts for the model
        # version to local
        mv.download_directory_from_model_version(
            local_directory_path=settings.model_directory,
            neptune_attribute_path="model",
        )
    else:
        logger.info(
            f"The specified output directory {settings.model_directory} already "
            f"exists and is not empty: {os.listdir(settings.model_directory)}. Model "
            "download skipped."
        )
    # shutdown client
    mv.stop()


if __name__ == "__main__":
    init_logging(cast(settings, OnclusiveLogSettings))
    download_model(settings)
