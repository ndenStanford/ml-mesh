"""Utils for integration test."""

# Standard Library
import time

# 3rd party libraries
import boto3
import pandas as pd

# Internal libraries
from onclusiveml.core.logging import get_default_logger

# Source
from src.settings import get_settings


settings = get_settings()

logger = get_default_logger(__name__)
# Initialize a session
session = boto3.session.Session(
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.REGION_NAME,
)


def execute_sql_statement(session):
    """Exetuce SQL query on Redshift."""
    client = session.client("redshift-data")
    response = client.execute_statement(
        ClusterIdentifier=settings.CLUSTER_ID,
        Database=settings.DATABASE,
        DbUser=settings.DB_USER,
        Sql=settings.SQL,
    )
    return response


def retrieve_response(response):
    """Retrieve queried dataset."""
    client = session.client("redshift-data")
    execution_id = response["Id"]
    status = client.describe_statement(Id=execution_id)["Status"]
    while status not in ["FINISHED", "ABORTED", "FAILED"]:
        time.sleep(10)
        status = client.describe_statement(Id=execution_id)["Status"]
    logger.debug(f"Execution {execution_id} finished with status {status}")

    if status == "FINISHED":
        columns = [
            c["label"]
            for c in client.get_statement_result(Id=execution_id)["ColumnMetadata"]
        ]
        records = client.get_statement_result(Id=execution_id)["Records"]
        logger.debug(f"SUCCESS. Found {len(records)} records")
    else:
        logger.debug(
            f'Failed with Error: {client.describe_statement(Id=execution_id)["Error"]}'
        )

    dataframe_dict = dict()
    for record in records:
        for index, r in enumerate(record):
            element_tuple = list(r.items())[0]
            element_value = element_tuple[1]
            column_name = columns[index]
            dataframe_dict[column_name] = dataframe_dict.get(column_name, []) + [
                element_value
            ]

    df = pd.DataFrame.from_dict(dataframe_dict)
    return df


def retrieve_redshift_dataframe():
    """Retrieve summarization dataframe."""
    response = execute_sql_statement(session)
    df = retrieve_response(response)
    return df
