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
        level=os.environ["IPTC_LEVEL"],
        num_shards=int(os.environ["SHARDS"]),
        test=True,
    )
    _, err = capsys.readouterr()
    assert err == ""
    s3 = boto3.resource("s3")
    target_bucket = s3.Bucket(os.environ["TARGET_BUCKET"])
    response = target_bucket.objects.filter(Prefix=os.environ["IPTC_LEVEL"]).delete()
    _, err = capsys.readouterr()
    assert err == ""
    assert response[0]["ResponseMetadata"]["HTTPStatusCode"] == 200
