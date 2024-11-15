"""Topic summarization report generator."""

# Standard Library
from datetime import date, timedelta
from typing import Optional

# 3rd party libraries
from boto3.dynamodb.conditions import Key
from fastapi import APIRouter, HTTPException

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel

# Source
from src.serve.tables import TopicSummaryDynamoDB


# map category in LLM output to real category
IMPACT_CATEGORIES = {
    "opportunities": "Opportunities",
    "risk": "Risk detection",
    "threats": "Threats for the brand",
    "company": "Company or spokespersons",
    "brand": "Brand Reputation",
    "ceo": "CEO Reputation",
    "customer": "Customer Response",
    "stock": "Stock Price Impact",
    "industry": "Industry trends",
    "environment": "Environmental, social and governance",
}


def get_topic_summarization_report_router() -> APIRouter:
    """Create a router for fetching filtered topic summarization reports."""
    # Initialize a FastAPI router
    router = APIRouter()
    # Initialize the DynamoDB model
    response_model = DynamoDBModel(model=TopicSummaryDynamoDB)

    # Define the route for the report
    @router.get("/topic-summarization/report")
    async def get_filtered_report(
        start_date: date, end_date: date, query_string: Optional[str] = None
    ):
        try:
            # Fetch all items from DynamoDB
            all_items = []
            current_date = start_date
            while current_date <= end_date:
                # Fetch results for the current date using get_query
                key_condition = Key("timestamp_date").eq(current_date.isoformat())
                db_query = {"hash_key": key_condition, "index": "timestamp_date-index"}
                query_results = response_model.get_query(search_query=db_query)
                all_items.extend(query_results)

                while "LastEvaluatedKey" in query_results:
                    db_query = {
                        "hash_key": key_condition,
                        "index": "timestamp_date-index",
                        "last_evaluated_key": query_results.get("LastEvaluatedKey"),
                    }
                    query_results = response_model.get_query(search_query=db_query)
                    all_items.extend(query_results)

                current_date += timedelta(days=1)
            # Apply filtering based on query_profile, topic_id, and time range
            if query_string:
                filtered_items = [
                    item
                    for item in all_items
                    if (
                        (item["trending"] is True)
                        and (item["query_string"] == query_string)
                    )
                ]
            else:
                filtered_items = [
                    item for item in all_items if item["trending"] is True
                ]
            report_list = [
                {
                    "Query": item["query_string"],
                    "Topic Id": item["topic_id"],
                    "Run Date": item["timestamp_date"],
                    "Theme": item["analysis"]["theme"],
                    "Summary": item["analysis"]["summary"],
                    "Sentiment": item["analysis"]["sentiment"],
                    "Entity Impact": item["analysis"]["entity_impact"],
                    "Leading Journalist": item["analysis"]["lead_journalists"],
                    "Topic": {
                        IMPACT_CATEGORIES[key]: {
                            "Summary": item["analysis"][key]["summary"],
                            "Theme": item["analysis"][key]["theme"],
                            "Impact": item["analysis"][key]["impact"],
                        }
                        for key in IMPACT_CATEGORIES.keys()
                    },
                }
                for item in filtered_items
            ]
            # Return the filtered items as a JSON response
            return report_list

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return router
