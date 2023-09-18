"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import apache_beam as beam
import boto3
import pyarrow
from apache_beam.io import ReadFromText, WriteToParquet


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

    with beam.Pipeline() as p:
        for obj in s3.Bucket(source_bucket_name).objects.all():
            target_key = (
                obj.key.replace("csv", "parquet").replace("raw", "test")
                if test
                else obj.key.replace("csv", "parquet").replace("raw", "iptc")
            )
            _ = (
                p
                | ReadFromText(f"s3://{source_bucket_name}/{obj.key}")
                | WriteToParquet(
                    f"s3://{target_bucket_name}/{target_key}",
                    schema=pyarrow.schema(
                        [
                            ("topic_1", pyarrow.string()),
                            ("topic_2", pyarrow.string()),
                            ("title", pyarrow.string()),
                            ("language", pyarrow.string()),
                            ("content", pyarrow.string()),
                        ]
                    ),
                )
            )
            if test:
                break
    # for obj in s3.Bucket(source_bucket_name).objects.all():
    #     current_object = obj.get()
    #     _, sub_dir, filename = obj.key.split("/")
    #     df_pa = csv.read_csv(
    #         current_object["Body"],
    #         parse_options=csv.ParseOptions(invalid_row_handler=lambda x: "skip"),
    #     )
    #     pq.write_table(
    #         table=df_pa,
    #         where=f"s3://{target_bucket_name}/iptc/{sub_dir}/{filename.replace('csv', 'parquet')}"
    #         if not test
    #         else f"s3://{target_bucket_name}/test/{sub_dir}/{filename.replace('csv', 'parquet')}",
    #     )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
    )
