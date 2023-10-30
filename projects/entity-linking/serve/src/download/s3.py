"""Helpers."""

# Standard Library
import os
from typing import Any


def sync_folder(
    client: Any, bucket: str, source_folder: str, target_folder: str
) -> None:
    """Syncronize folder from S3 bucket to local.

    Args:
        client (Any): Boto3 s3 client.
        bucket (str): source data bucket.
        source_folder (str): source data path in bucket.
        target_folder (str): target folder on process runner system.
    """
    objects = client.list_objects_v2(Bucket=bucket, Prefix=source_folder).get(
        "Contents", []
    )

    for obj in objects:
        *_, folder, filename = obj["Key"].split("/")

        if not os.path.exists(
            os.path.dirname(os.path.join(target_folder, folder, filename))
        ):
            os.makedirs(os.path.dirname(os.path.join(target_folder, folder, filename)))

        with open(os.path.join(target_folder, folder, filename), "wb") as f:
            client.download_fileobj(bucket, obj["Key"], f)
