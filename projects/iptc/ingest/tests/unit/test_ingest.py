"""Unit tests."""

# Standard Library
import os

# 3rd party libraries
import boto3

# Source
from src.ingest import ingest


def test_ingest(capsys) -> None:
    """Ingest and then delete a single file from the source bucket to the target bucket.

    Args:
        capsys : Capture stdout/stderr output
    """
    ingest(
        source_bucket_name=os.environ["SOURCE_BUCKET"],
        target_bucket_name=os.environ["TARGET_BUCKET"],
        test=True,
    )
    _, err = capsys.readouterr()
    assert err == ""
    s3 = boto3.resource("s3")
    target_bucket = s3.Bucket(os.environ["TARGET_BUCKET"])
    response = target_bucket.objects.filter(Prefix="test").delete()
    _, err = capsys.readouterr()
    assert err == ""
    assert response[0]["ResponseMetadata"]["HTTPStatusCode"] == 200
