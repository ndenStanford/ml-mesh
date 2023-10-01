"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import apache_beam as beam
import pyarrow as pa
from apache_beam.dataframe.convert import to_pcollection
from apache_beam.dataframe.io import read_csv


# from src.settings import SCHEMA_MAP


# from onclusiveml.data.ingestion.csvio import ReadCsvsFromS3


def ingest(
    source_bucket_name: str,
    target_bucket_name: str,
    level: str,
    num_shards: int,
    test: bool,
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        level (str): IPTC dataset level, can be one of:
            {'first_level', 'first_level_multi_lingual','second_level',
            'second_level_multi_lingual', 'third_level', 'third_level_multi_lingual'}
        num_shards (int): The number of files (shards) used for output, default 3000.
        test (bool): Test flag
    """
    # schema = SCHEMA_MAP[level]
    target_path = (
        f"s3://{target_bucket_name}/iptc/{level}/ingested"
        if not test
        else f"s3://{target_bucket_name}/test/{level}/ingested"
    )
    # with beam.Pipeline() as p:
    #     _ = (
    #         p
    #         | "Read CSV" >> ReadCsvsFromS3(f"s3://{source_bucket_name}/raw/{level}/")
    #         | "Write parquet"
    #         >> beam.io.WriteToParquet(
    #             file_path_prefix=target_path,
    #             file_name_suffix=".parquet",
    #             schema=pa.schema(schema.schema_dict),
    #             num_shards=num_shards,
    #         )
    #     )
    with beam.Pipeline() as p:
        df = p | "Read CSV" >> read_csv(f"s3://{source_bucket_name}/raw/{level}/*.csv")
        pcoll = to_pcollection(df, include_indexes=False, yield_elements="pandas")
        _ = (
            pcoll
            | "To table"
            >> beam.Map(lambda x: pa.Table.from_pandas(x, preserve_index=False))
            | "Write to Parquet Batched"
            >> beam.io.WriteToParquetBatched(
                file_path_prefix=target_path,
                file_name_suffix=".parquet",
                num_shards=num_shards,
            )
        )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        level=os.environ["IPTC_LEVEL"],
        num_shards=int(os.environ["SHARDS"]),
        test=False,
    )
