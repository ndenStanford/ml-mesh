"""Compile ingest pipeline."""

# Standard Library
import os
from datetime import datetime

# 3rd party libraries
import boto3
from kfp.compiler import Compiler
from kfp.v2.dsl import pipeline

# Source
from src.components.ingest import ingest


@pipeline
def ingest_pipeline(source_bucket: str, target_bucket: str) -> None:
    """Ingesting pipeline.

    Args:
        source_bucket (str): S3 bucket name with source, raw data
        target_bucket (str): S3 bucket name with target, ingested data
    """
    _ = (
        ingest(source_bucket=source_bucket, target_bucket=target_bucket)
        .set_env_variable("AWS_ACCESS_KEY_ID", os.environ.get("AWS_ACCESS_KEY_ID"))
        .set_env_variable(
            "AWS_SECRET_ACCESS_KEY", os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
    )


if __name__ == "__main__":
    compiled_name = f"iptc_ingest_{datetime.now().strftime('%Y%m%d%H%M%S')}.yaml"
    Compiler().compile(pipeline_func=ingest_pipeline, package_path=compiled_name)
    s3_client = boto3.client("s3")
    s3_client.upload_file(
        compiled_name, os.environ.get("COMPILED_PIPELINES"), compiled_name
    )
