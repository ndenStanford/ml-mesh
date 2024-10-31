"""Topic summarization report generator."""

# 3rd party libraries

# Standard Library
from datetime import date, timedelta

# 3rd party libraries
from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, HTTPException

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel

# Source
from src.serve.tables import TopicSummaryDynamoDB


def get_topic_summarization_report_router() -> APIRouter:
    """Create a router for fetching filtered topic summarization reports."""
    # Initialize a FastAPI router
    router = APIRouter()
    # Initialize the DynamoDB model
    response_model = DynamoDBModel(model=TopicSummaryDynamoDB)

    # Define the route for the report
    @router.get("/topic-summarization/report")
    async def get_filtered_report(
        start_date: date,
        end_date: date,
    ):
        try:
            # Fetch all items from DynamoDB
            all_items = []
            current_date = start_date
            while current_date <= end_date:
                # Fetch results for the current date using get_query
                key_condition = Key("timestamp_date").eq(current_date.isoformat())
                db_query = {"hash_key": key_condition, "index": "timestamp_date-index"}
                query_results = response_model.get_query(db_query=db_query)
                all_items.extend(query_results)
                # print("**********")
                # print("**********")
                # print("**********")
                # print("FIRST ALL ITEM LENTGH :", len(all_items))

                while "LastEvaluatedKey" in query_results:
                    db_query = {
                        "hash_key": key_condition,
                        "index": "timestamp_date-index",
                        "last_evaluated_key": query_results.get("LastEvaluatedKey"),
                    }
                    query_results = response_model.get_query(db_query=db_query)
                    all_items.extend(query_results)
                # all_items.extend(query_results)  # Combine results from each day
                # print("**********")
                # print("**********")
                # print("**********")
                # print("SECOND ALL ITEM LENTGH :", len(all_items))

                current_date += timedelta(days=1)
            # Apply filtering based on query_profile, topic_id, and time range
            filtered_items = [item for item in all_items if item["trending"] is True]
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
