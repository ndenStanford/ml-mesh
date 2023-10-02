"""Ingest component."""

# Standard Library
import csv
import os

# 3rd party libraries
import apache_beam as beam
import pyarrow as pa
from apache_beam.dataframe.convert import to_pcollection
from apache_beam.dataframe.io import read_csv
from pyarrow import fs
from pyarrow import parquet as pq


def ingest(
    source_bucket_name: str,
    target_bucket_name: str,
    level: str,
    test: bool,
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        level (str): IPTC dataset level, can be one of:
            {'first_level', 'first_level_multi_lingual','second_level',
            'second_level_multi_lingual', 'third_level', 'third_level_multi_lingual'}
        test (bool): Test flag
    """
    target_path = (
        f"s3://{target_bucket_name}/iptc/{level}/ingested"
        if not test
        else f"s3://{target_bucket_name}/test/{level}/ingested"
    )
    s3 = fs.S3FileSystem()
    with beam.Pipeline() as p:
        dfs = p | "Read CSV" >> read_csv(
            f"s3://{source_bucket_name}/raw/{level}/*.csv",
            engine="c",
            lineterminator="\n",
            quoting=csv.QUOTE_NONNUMERIC,
        )
        pcoll_df = to_pcollection(dfs, include_indexes=False, yield_elements="pandas")
        _ = (
            pcoll_df
            | "To table"
            >> beam.Map(lambda x: pa.Table.from_pandas(x, preserve_index=False))
            | "Combine" >> beam.combiners.ToList()
            | "To parquet"
            >> beam.Map(
                lambda seq: [
                    pq.write_table(table, f"{target_path}-{idx}.parquet", filesystem=s3)
                    for idx, table in enumerate(seq)
                ]
            )
        )


if __name__ == "__main__":
    # Standard Library
    import faulthandler

    faulthandler.enable()
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        level=os.environ["IPTC_LEVEL"],
        test=False,
    )
