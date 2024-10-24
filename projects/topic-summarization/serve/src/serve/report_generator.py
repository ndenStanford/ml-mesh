"""Topic summarization report generator."""

# 3rd party libraries
# Standard Library
from datetime import datetime

from fastapi import APIRouter, HTTPException

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel

from src.serve.tables import TopicSummaryResponseDB


def get_topic_summarization_report_router() -> APIRouter:
    """Create a router for fetching filtered topic summarization reports."""
    # Initialize a FastAPI router
    router = APIRouter()

    # Initialize the DynamoDB model
    response_model = DynamoDBModel(model=TopicSummaryResponseDB)

    # Define the route for the report
    @router.get("/topic-summarization/report")
    async def get_filtered_report(
        query_string: str,
        topic_id: int,
        start_time: datetime,
        end_time: datetime,
    ):
        try:
            # Fetch all items from DynamoDB
            all_items = response_model.get_all()

            # Apply filtering based on query_profile, topic_id, and time range
            filtered_items = [
                item
                for item in all_items
                if item["query_string"] == query_string
                and item["topic_id"] == topic_id
                and item["trending"] is True
                and (start_time is None or item["timestamp"] >= start_time)
                and (end_time is None or item["timestamp"] <= end_time)
            ]
            report_list = [
                {
                    "Query": item["query_string"],
                    "Topic": item["topic_id"],
                    "Run Date": item["timestamp_date"],
                    "Theme": item["analysis"]["theme"],
                    "Summary": item["analysis"]["summary"],
                    "Sentiment": item["analysis"]["sentiment"],
                    "Entity Impact": item["analysis"]["entity_impact"],
                    "Leading Journalist": item["analysis"]["lead_journalists"],
                }
                for item in filtered_items
            ]

            # Return the filtered items as a JSON response
            return report_list

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
