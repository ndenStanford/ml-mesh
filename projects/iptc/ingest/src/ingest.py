"""Ingest component."""

# Standard Library
import csv
from datetime import datetime

# 3rd party libraries
import apache_beam as beam
import pyarrow as pa
from apache_beam.dataframe.convert import to_pcollection
from apache_beam.dataframe.io import read_csv
from apache_beam.io.parquetio import WriteToParquetBatched
from pydantic import BaseSettings

# Source
from src.settings import get_settings  # type: ignore[attr-defined]


def ingest(settings: BaseSettings) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        settings (BaseSettings): Settings class

    """
    with beam.Pipeline() as p:
        dfs = p | "Read CSVs" >> read_csv(
            settings.source_path,
            engine="c",
            usecols=settings.schema,
            lineterminator="\n",
            quoting=csv.QUOTE_NONNUMERIC,
            chunksize=128,
            iterator=True,
        )
        pcoll_df = to_pcollection(dfs, include_indexes=False, yield_elements="pandas")
        _ = (
            pcoll_df
            | "Fill NaN" >> beam.Map(lambda x: x.fillna("nan"))
            | "Add id and timestamp columns"
            >> beam.Map(
                lambda x: x.assign(
                    id=x.apply(lambda y: hash(tuple(y)), axis=1),
                    timestamp=datetime.now(),
                )
            )
            | "Transform to tables"
            >> beam.Map(lambda x: pa.Table.from_pandas(x, preserve_index=False))
            | "Write to parquet files"
            >> WriteToParquetBatched(
                file_path_prefix=settings.target_path,
                file_name_suffix=".parquet",
                num_shards=settings.shards,
                shard_name_template=f"-{len(str(settings.shards))*'S'}",
                schema=pa.schema(
                    [(k, pa.string()) for k in settings.schema]
                    + [("id", pa.int64()), ("timestamp", pa.timestamp("ns"))]
                ),
            )
        )


if __name__ == "__main__":
    settings = get_settings()
    ingest(settings)
