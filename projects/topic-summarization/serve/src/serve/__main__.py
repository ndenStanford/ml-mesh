# type: ignore
"""Model server."""

# Internal libraries
from onclusiveml.data.data_model.dynamodb_data_model.dynamodb_model import (
    DynamoDBModel,
)
from onclusiveml.serving.rest.crud.dynamodb_router import DynamoDBCRUDRouter
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve._init import init
from src.serve.model import ServedTopicModel
from src.serve.tables import PredictResponseSchemaWID, TopicSummaryResponseDB


def get_model_server() -> ModelServer:
    """Utility method for prepping a fully configured model server instance ready to serve."""
    # initialize model
    topic_served_model = ServedTopicModel()
    # initialize model server
    serving_params = ServingParams()

    model_server = ModelServer(
        configuration=serving_params, model=topic_served_model, on_startup=[init]
    )
    Instrumentator.enable(model_server, app_name="topic-summarization")

    response_model = DynamoDBModel(model=TopicSummaryResponseDB)
    model_server.include_router(
        DynamoDBCRUDRouter(
            schema=PredictResponseSchemaWID,
            model=response_model,
            create_schema=PredictResponseSchemaWID,
            update_schema=PredictResponseSchemaWID,
            prefix="/items",
            tags=["Items"],
            delete_one_route=False,
            delete_all_route=False,
        )
    )

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
