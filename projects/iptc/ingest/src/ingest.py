"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import boto3
from pyarrow import csv
from pyarrow import parquet as pq


def ingest(source_bucket_name: str, target_bucket_name: str) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
    """
    s3 = boto3.resource("s3")

    for obj in s3.Bucket(source_bucket_name).objects.all():
        current_object = obj.get()
        _, sub_dir, filename = obj.key.split("/")
        df_pa = csv.read_csv(
            current_object["Body"],
            parse_options=csv.ParseOptions(invalid_row_handler=lambda x: "skip"),
        )
        pq.write_table(
            df_pa,
            f"s3://{target_bucket_name}/iptc/{sub_dir}/{filename.replace('csv', 'parquet')}",
        )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
    )
