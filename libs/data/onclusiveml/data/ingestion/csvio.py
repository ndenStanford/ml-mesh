"""Beam transform class to read csvs."""

# Standard Library
import codecs
import csv
import sys
from typing import Iterator

# 3rd party libraries
import apache_beam as beam
from apache_beam.io.aws.s3io import S3IO


csv.field_size_limit(sys.maxsize)


def iterate_s3io_bucket_items(path: str, client: S3IO) -> Iterator[str]:
    """Generator of filenames in the provided s3 `path`.

    Args:
        path (str): S3 path
        client (S3IO): S3 IO client

    Yields:
        atr: file name
    """
    for file_name, _ in client.list_files(path):
        yield file_name


class ReadCsvsFromS3(beam.PTransform):
    """A :class:`~apache_beam.transforms.ptransform.PTransform` for reading csv files.

    It outputs a :class:`~apache_beam.pvalue.PCollection` of
    ``dict:s``, each corresponding to a row in the csv file.

    Args:
        csvs_path (str): Path to the CSVs.

    Examples:
        Reading content of a s3 directory with csv files. ::

            import apache_beam as beam
            from apache_beam.options.pipeline_options import PipelineOptions
            from onclusiveml.data.ingestion.csvio import ReadCsvsFromS3

            path_to_csv = 's3://path/to/csvs/'
            with beam.Pipeline(options=PipelineOptions()) as p:
                _ = p | "Reading csvs' records" >> ReadCsvsFromS3(path_to_csv)
                        | 'Writing to stdout' >> beam.Map(print)

        The output will be something like ::

            {'lastName': 'Norvell', 'firstName': 'Andrel', 'level': '10'}
            {'lastName': 'Proudfoot', 'firstName': 'Dinorah', 'level': '8'}
            {'lastName': 'Plotkin', 'firstName': 'Trulal', 'level': '14'}

    """

    def __init__(self, csvs_path: str):
        super(ReadCsvsFromS3, self).__init__()
        self._csvs_path = csvs_path

    def expand(self, pcoll: beam.PCollection) -> beam.pvalue.PCollection:
        """Expands the beam.io.Read.

        Args:
            pcoll (beam.PCollection): Input PCollection

        Returns:
            beam.pvalue.PCollection
        """
        return pcoll | beam.io.Read(_CsvSource(self._csvs_path))


class _CsvSource(beam.io.filebasedsource.FileBasedSource):
    def read_records(
        self, csvs_path: str, range_tracker: beam.io.OffsetRangeTracker
    ) -> Iterator[dict]:
        s3io_client = S3IO(options={})
        items = iterate_s3io_bucket_items(csvs_path, s3io_client)
        for item in items:
            with s3io_client.open(item) as f:
                reader = csv.DictReader(
                    codecs.iterdecode(f, "utf-8"), quoting=csv.QUOTE_ALL
                )
                for rec in reader:
                    yield {k: v.replace("\n", "") for k, v in rec.items()}
