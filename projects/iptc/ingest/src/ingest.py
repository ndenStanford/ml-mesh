"""Ingest component."""
# Standard libraries

# Standard Library
import os

# 3rd party libraries
import boto3


def ingest(source_bucket: str, target_bucket: str) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket (str): S3 bucket name with source, raw data
        target_bucket (str): S3 bucket name with target, ingested data
    """
    # Retrieve the list of existing buckets
    s3 = boto3.client("s3")
    response = s3.list_buckets()
    # Output the bucket names
    print("Existing buckets:")
    for bucket in response["Buckets"]:
        print(f'  {bucket["Name"]}')


if __name__ == "__main__":
    ingest(
        source_bucket=os.environ["SOURCE_BUCKET"],
        target_bucket=os.environ["TARGET_BUCKET"],
    )
