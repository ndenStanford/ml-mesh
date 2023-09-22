"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import apache_beam as beam
import pyarrow as pa

# Internal libraries
from onclusiveml.data.ingestion.csvio import ReadCsvsFromS3

# Source
from src.settings import SCHEMA_MAP


# from src.csvio import ReadCsvsFromS3


def ingest(
    source_bucket_name: str,
    target_bucket_name: str,
    level: str,
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        level (str): IPTC dataset level, can be one of:
            {'first_level', 'first_level_multi_lingual','second_level',
            'second_level_multi_lingual', 'third_level', 'third_level_multi_lingual'}
    """
    schema = SCHEMA_MAP[level]
    with beam.Pipeline() as p:
        _ = (
            p
            | "Read CSVs" >> ReadCsvsFromS3(f"s3://{source_bucket_name}/raw/{level}/")
            | "Write to parquet"
            >> beam.io.WriteToParquet(
                file_path_prefix=f"s3://{target_bucket_name}/iptc/{level}/parquet",
                file_name_suffix=".parquet",
                schema=pa.schema(schema.schema_dict),
            )
        )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        level=os.environ["IPTC_LEVEL"],
    )
