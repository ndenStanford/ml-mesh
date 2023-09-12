"""Ingest component."""

# 3rd party libraries
from kfp.v2.dsl import Dataset, Output, component


@component(
    base_image="python:3.8.16",
    packages_to_install=["pyarrow>=13.0.0", "boto3>=1.28.45"],
)
def ingest(
    source_bucket: str, target_bucket: str, ingested_data: Output[Dataset]
) -> None:
    """Read the opoint data, write to the data lake bucket in .parquet.

    Args:
        source_bucket (str): S3 bucket name with source, raw data
        target_bucket (str): S3 bucket name with target, ingested data
        ingested_data (Output[Dataset]): Kubeflow dataset
    """
    pass
