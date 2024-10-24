# type: ignore
# isort: skip_file

"""Model server."""

# Internal libraries
from onclusiveml.data.data_model.dynamodb import DynamoDBModel
from onclusiveml.serving.rest.crud._base import CRUDGenerator
from onclusiveml.serving.rest.observability import Instrumentator
from onclusiveml.serving.rest.serve import ModelServer, ServingParams

# Source
from src.serve._init import init
from src.serve.model import ServedTopicModel
from src.serve.report_generator import get_topic_summarization_report_router
from src.serve.schema import PredictResponseSchema
from src.serve.tables import PredictResponseSchemaWID, TopicSummaryResponseDB
from src.settings import get_settings


settings = get_settings()


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
        CRUDGenerator(
            schema=PredictResponseSchemaWID,
            model=response_model,
            create_schema=PredictResponseSchema,
            update_schema=PredictResponseSchema,
            api_settings=settings,
            tags=["Items"],
            delete_one_route=False,
            delete_all_route=False,
        )
    )

    model_server.include_router(get_topic_summarization_report_router())

    return model_server


model_server = get_model_server()

if __name__ == "__main__":
    # launch server process(es)
    model_server.serve()
