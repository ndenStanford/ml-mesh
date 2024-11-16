# type: ignore
# isort: skip_file

"""Model server."""
# Standard Library
import json
from datetime import date, timedelta
from typing import Optional

# 3rd party libraries
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.testclient import TestClient

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel
from onclusiveml.serving.rest.crud._base import CRUDGenerator
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve._init import init
from src.serve.model import ServedTopicModel

# from src.serve.report_generator import get_topic_summarization_report_router
from src.serve.schema import PredictResponseSchema
from src.serve.tables import PredictResponseSchemaWID, TopicSummaryResponseDB
from src.settings import get_settings


settings = get_settings()

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


def get_crud_router() -> CRUDGenerator:
    """Define CRUD Router."""
    response_model = DynamoDBModel(model=TopicSummaryResponseDB)
    return CRUDGenerator(
        schema=PredictResponseSchemaWID,
        model=response_model,
        create_schema=PredictResponseSchema,
        update_schema=PredictResponseSchema,
        api_settings=settings,
        entity_name="topic-summary-document",
        tags=["Items"],
        delete_one_route=False,
        delete_all_route=False,
        get_query_route=True,
    )


def get_topic_summarization_report_router() -> APIRouter:
    """Create a router for fetching filtered topic summarization reports."""
    # Initialize a FastAPI router
    router = APIRouter()
    crud_router = get_crud_router()
    app = FastAPI()
    app.include_router(crud_router)

    client = TestClient(app)

    # Initialize the DynamoDB model
    # response_model = DynamoDBModel(model=TopicSummaryDynamoDB)
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
                key_condition = 'Key("timestamp_date").eq(current_date.isoformat())'
                db_query = {"hash_key": key_condition, "index": "timestamp_date-index"}

                serialized_query = json.dumps(db_query)
                # Use the global `client` to make a GET request
                response = client.get(
                    "/topic-summary-document/query",
                    params={"serialized_query": serialized_query},
                )
                query_results = response.json()
                # query_results = response_model.get_query(search_query=db_query)
                all_items.extend(query_results)

                while "LastEvaluatedKey" in query_results:
                    db_query = {
                        "hash_key": key_condition,
                        "index": "timestamp_date-index",
                        "last_evaluated_key": query_results.get("LastEvaluatedKey"),
                    }
                    serialized_query = json.dumps(db_query)
                    response = client.get(
                        "/topic-summary-document/query",
                        params={"serialized_query": serialized_query},
                    )
                    query_results = response.json()
                    # query_results = response_model.get_query(search_query=db_query)
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


def get_model_server() -> ModelServer:
    """Utility method for preparing a fully configured model server instance ready to serve."""
    # initialize model
    topic_served_model = ServedTopicModel()
    # initialize model server
    serving_params = ServingParams()

    model_server = ModelServer(
        configuration=serving_params, model=topic_served_model, on_startup=[init]
    )
    Instrumentator.enable(model_server, app_name="topic-summarization")

    # response_model = DynamoDBModel(model=TopicSummaryResponseDB)
    # model_server.include_router(
    #     CRUDGenerator(
    #         schema=PredictResponseSchemaWID,
    #         model=response_model,
    #         create_schema=PredictResponseSchema,
    #         update_schema=PredictResponseSchema,
    #         api_settings=settings,
    #         entity_name="topic-summary-document",
    #         tags=["Items"],
    #         delete_one_route=False,
    #         delete_all_route=False,
    #         get_query_route=True,
    #     )
    # )

    model_server.include_router(get_crud_router())
    model_server.include_router(get_topic_summarization_report_router())

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
