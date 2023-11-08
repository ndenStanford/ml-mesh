"""Unit tests."""

# Standard Library
import os

# 3rd party libraries
import boto3

# Source
from src.ingest import ingest
from src.settings import get_settings


def test_ingest(capsys) -> None:
    """Ingest and then delete a single file from the source bucket to the target bucket.

    Args:
        capsys : Capture stdout/stderr output
    """
    settings = get_settings()
    os.environ["IPTC_LEVEL"] = "first_level_multi_lingual_top_n"
    ingest(settings)
    _, err = capsys.readouterr()
    assert err == ""
    s3 = boto3.resource("s3")
    target_bucket = s3.Bucket(os.environ["TARGET_BUCKET"])
    _ = target_bucket.objects.filter(Prefix=os.environ["IPTC_LEVEL"]).delete()
    _, err = capsys.readouterr()
    assert err == ""
