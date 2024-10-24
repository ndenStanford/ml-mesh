"""Topic summarization report generator."""

# 3rd party libraries
# Standard Library
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

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
        query_profile: str,
        topic_id: str,
        start_time: Optional[datetime] = Query(None, description="Start of time range"),
        end_time: Optional[datetime] = Query(None, description="End of time range"),
    ):
        try:
            # Step 1: Fetch all items from DynamoDB
            all_items = response_model.get_all()

            # Step 2: Apply filtering based on query_profile, topic_id, and time range
            filtered_items = [
                item
                for item in all_items
                if item["query_profile"] == query_profile
                and item["topic_id"] == topic_id
                and (
                    start_time is None
                    or datetime.fromisoformat(item["timestamp"]) >= start_time
                )
                and (
                    end_time is None
                    or datetime.fromisoformat(item["timestamp"]) <= end_time
                )
            ]

            # Step 3: Return the filtered items as a JSON response
            return {"filtered_items": filtered_items}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
