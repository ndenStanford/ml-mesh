"""Ingest component."""

# Standard Library
import os

# 3rd party libraries
import apache_beam as beam
import boto3


# import pyarrow


# def str_to_dict(string: str) -> dict:
#     return {n: i for i, n in enumerate(string.split(","))}


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
            target_key = obj.key.replace(".csv", "", 1)
            target_key = (
                target_key.replace("raw", "test", 1)
                if test
                else target_key.replace("raw", "iptc", 1)
            )
            csv_file = p | beam.dataframe.io.read_csv(
                f"s3://{source_bucket_name}/{obj.key}",
                usecols=["title", "score", "topic", "content", "summary"],
                index_col=False,
            )
            csv_file.to_parquet(f"s3://{target_bucket_name}/{target_key}", index=False)
            if test:
                break
            #     | beam.io.parquetio.WriteToParquet(
            #         file_path_prefix=f"s3://{target_bucket_name}/{target_key}",
            #         file_name_suffix=".parquet",
            #         schema=pyarrow.schema(
            #             [
            #                 pyarrow.field("title", pyarrow.string()),
            #                 pyarrow.field("score", pyarrow.float64()),
            #                 pyarrow.field("topic", pyarrow.string()),
            #                 pyarrow.field("content", pyarrow.string()),
            #                 pyarrow.field("summary", pyarrow.string()),
            #             ]
            #         ),
            #     )
            # )
            # | beam.io.ReadFromText(
            #     f"s3://{source_bucket_name}/{obj.key}",
            # )
            # | beam.Map(lambda item: item.split(','))
            # | beam.Map(lambda item: print(item))
            # | beam.Map(lambda item: print(len(item)))
            # | beam.io.WriteToParquet(
            #     f"s3://{target_bucket_name}/{target_key}",
            #     schema=pyarrow.schema(
            #         [
            #             ("Unnamed: 0", pyarrow.int64()),
            #             ("title", pyarrow.string()),
            #             ("score", pyarrow.float64()),
            #             ("topic", pyarrow.string()),
            #             ("content", pyarrow.string()),
            #             ("summary", pyarrow.string()),
            #         ]
            #     ),
            # )
    # Brute force:
    #
    # for obj in s3.Bucket(source_bucket_name).objects.all():
    #     target_key = (
    #         obj.key.replace("csv", "parquet", 1).replace("raw", "test", 1)
    #         if test
    #         else obj.key.replace("csv", "parquet", 1).replace("raw", "iptc", 1)
    #     )
    #     current_object = obj.get()
    #     _, sub_dir, filename = obj.key.split("/")
    #     df_pa = csv.read_csv(
    #         current_object["Body"],
    #         parse_options=csv.ParseOptions(invalid_row_handler=lambda x: "skip"),
    #     )
    #     pq.write_table(
    #         table=df_pa,
    #         where=f"s3://{target_key}"
    #     )


if __name__ == "__main__":
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
    )
