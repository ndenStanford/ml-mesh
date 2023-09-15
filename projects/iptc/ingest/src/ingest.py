"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import boto3
from pyarrow import csv
from pyarrow import parquet as pq


def ingest(
    source_bucket_name: str, target_bucket_name: str, test: bool = False
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        test (bool): Flag to break the loop and clean, default False
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
            table=df_pa,
            where=f"s3://{target_bucket_name}/iptc/{sub_dir}/{filename.replace('csv', 'parquet')}"
            if not test
            else f"s3://{target_bucket_name}/test/{sub_dir}/{filename.replace('csv', 'parquet')}",
        )
        if test:
            break


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
    )
