"""Ingest component."""

# Standard Library
import csv
import os
import typing

# 3rd party libraries
import apache_beam as beam

# Source
from src.settings import SCHEMA_MAP


class Read(beam.PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading csv files.

    It outputs a :class:`~apache_beam.pvalue.PCollection` of
    ``dict:s``, each corresponding to a row in the csv file.

    Args:
        csv_path (str): csv file path.

    Examples:
        Reading content of a csv file. ::

            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from beam_nuggets.io import csvio

            path_to_csv = '/path/to/students.csv'
            with beam.Pipeline(options=PipelineOptions()) as p:
                students = p | "Reading students records" >> csvio.Read(path_to_csv)
                students | 'Writing to stdout' >> beam.Map(print)

        The output will be something like ::

            {'lastName': 'Norvell', 'firstName': 'Andrel', 'level': '10'}
            {'lastName': 'Proudfoot', 'firstName': 'Dinorah', 'level': '8'}
            {'lastName': 'Plotkin', 'firstName': 'Trulal', 'level': '14'}

    """

    def __init__(self, csv_path: str) -> None:
        super(Read, self).__init__()
        self._csv_path = csv_path

    def expand(self, pcoll: beam.PCollection) -> beam.PCollection:
        """expand."""
        return pcoll | beam.io.Read(_CsvSource(self._csv_path))


class _CsvSource(beam.io.filebasedsource.FileBasedSource):
    def read_records(self, file_name: str) -> typing.Generator:
        # FIXME handle concurrent read
        self._file = self.open_file(file_name)

        for rec in csv.DictReader(self._file):
            yield rec


def ingest(
    source_bucket_name: str,
    target_bucket_name: str,
    level: str,
    files: str = "doc_classification_dataset_crawler-4-2022-03_*.csv",
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket_name (str): S3 bucket name with source, raw data
        target_bucket_name (str): S3 bucket name with target, ingested data
        level (str): IPTC dataset level, can be one of:
            {'first_level', 'first_level_multi_lingual','second_level',
            'second_level_multi_lingual', 'third_level', 'third_level_multi_lingual'}
        files (str): Files to read
    """
    schema = SCHEMA_MAP[level]
    with beam.Pipeline() as p:
        _ = (
            p
            | "Read lines"
            >> Read(f"s3://{source_bucket_name}/raw/{schema.dir_name}/{files}")
            # | "Split" >> beam.Map(lambda item: csv.DictReader(StringIO(item)))
            | "Print" >> beam.Map(print)
        )
        # words = (
        #     lines
        #     |
        #     # | "Len" >> Map(len)
        #     # | "Print" >> Map(print)
        # )
        # p
        # | ReadFromText(f"s3://{source_bucket_name}/raw/{schema.dir_name}/*.csv")
        # | read_csv(
        #     f"s3://{source_bucket_name}/raw/{schema.dir_name}/*.csv",
        #     usecols=list(schema.schema_dict.keys()),
        #     index_col=False)
        # ) | Map(print)
        # | WriteToParquet(
        #     file_path_prefix=f"s3://{target_bucket_name}/iptc/{schema.dir_name}/",
        #     file_name_suffix=".parquet",
        #     schema=pa.schema([(k, v) for k, v in schema.schema_dict.items()]),
        # )
        # | WriteToParquet(
        #     file_path_prefix=f"s3://{target_bucket_name}/iptc/{schema.dir_name}/",
        #     file_name_suffix=".parquet",
        #     schema=pa.schema([(k, v) for k, v in schema.schema_dict.items()]),
        # )
        # | Map(
        #     lambda item: Row(
        #         title=item["title"],
        #         score=item["score"],
        #         topic=item["topic"],
        #         content=item["content"],
        #         summary=item["summary"],
        #     )
        # )
        # )
        # csv_file.to_parquet(
        #     f"s3://{target_bucket_name}/iptc/{schema.dir_name}/", index=False
        # )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        level=os.environ["IPTC_LEVEL"],
    )
