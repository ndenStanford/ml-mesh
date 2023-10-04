"""Ingest component."""

# Standard Library
import csv

# 3rd party libraries
import apache_beam as beam
import pyarrow as pa
from apache_beam.dataframe.convert import to_pcollection
from apache_beam.dataframe.io import read_csv
from pyarrow import fs
from pyarrow import parquet as pq
from pydantic import BaseSettings

# Source
from src.settings import get_settings  # type: ignore[attr-defined]


def ingest(settings: BaseSettings) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        settings (BaseSettings): Settings class

    """
    s3 = fs.S3FileSystem(region=fs.resolve_s3_region(settings.source_bucket))
    with beam.Pipeline() as p:
        dfs = p | "Read CSVs" >> read_csv(
            settings.source_path,
            engine="c",
            lineterminator="\n",
            quoting=csv.QUOTE_NONNUMERIC,
        )
        pcoll_df = to_pcollection(dfs, include_indexes=False, yield_elements="pandas")
        _ = (
            pcoll_df
            | "Transform to tables"
            >> beam.Map(lambda x: pa.Table.from_pandas(x, preserve_index=False))
            | "Combine" >> beam.combiners.ToList()
            | "Write to parquet files"
            >> beam.Map(
                lambda seq: [
                    pq.write_table(
                        table, f"{settings.target_path}-{idx}.parquet", filesystem=s3
                    )
                    for idx, table in enumerate(seq)
                ]
            )
        )


if __name__ == "__main__":
    settings = get_settings()
    ingest(settings)
