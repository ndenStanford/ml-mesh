"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
from apache_beam import Pipeline
from apache_beam.dataframe.io import read_csv

# Source
from src.settings import SCHEMA_MAP


def ingest(source_bucket_name: str, target_bucket_name: str, level: str) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        level (str): IPTC dataset level, can be one of:
            {'first_level', 'first_level_multi_lingual','second_level',
            'second_level_multi_lingual', 'third_level', 'third_level_multi_lingual'}
    """
    schema = SCHEMA_MAP[level]
    with Pipeline() as p:
        csv_file = p | read_csv(
            f"s3://{source_bucket_name}/raw/{schema.dir_name}/*.csv",
            usecols=list(schema.schema_dict.keys()),
            index_col=False,
        )
        csv_file.to_parquet(
            f"s3://{target_bucket_name}/iptc/{schema.dir_name}", index=False
        )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        level=os.environ["IPTC_LEVEL"],
    )
