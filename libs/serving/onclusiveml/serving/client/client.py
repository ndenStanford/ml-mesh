"""ML APIs client."""

# Standard Library
from typing import Any

# Internal libraries
import onclusiveml.serving.serialization.entity_linking.v1 as entity_linking_v1
import onclusiveml.serving.serialization.gch_summarization.v1 as gch_summarization_v1
import onclusiveml.serving.serialization.iptc.v1 as iptc_v1
import onclusiveml.serving.serialization.iptc_multi.v1 as iptc_multi_v1
import onclusiveml.serving.serialization.lsh.v1 as lsh_v1
import onclusiveml.serving.serialization.ner.v1 as ner_v1
import onclusiveml.serving.serialization.sentiment.v1 as sentiment_v1
import onclusiveml.serving.serialization.topic.v1 as topic_v1
import onclusiveml.serving.serialization.topic_summarization.v1 as topic_summarization_v1
from onclusiveml.models.iptc.class_dict import ID_TO_TOPIC
from onclusiveml.serving.client._bind import bind


class OnclusiveApiClient:
    """Onclusive Api client.

    Attributes:
        host (str): client hostnamne
        api_key (str): client api key.
        api_key_header (str): client api key header key.
        secure (bool): if yes, request is made through a secure endpoint.

    Example:
        >>> from onclusiveml.serving.client import OnclusiveApiClient
        >>> client = OnclusiveApiClient(host="internal.api.ml.stage.onclusive.com", api_key="")
        >>> output = client.ner(content="text to extract from")
    """

    def __init__(
        self,
        host: str,
        api_key: str,
        api_key_header: str = "x-api-key",
        secure: bool = True,
    ) -> None:
        self.protocol = "https" if secure else "http"
        self.host = host
        self.api_key_header = api_key_header
        self.api_key = api_key
        self.setup_iptc_bindings()

    def setup_iptc_bindings(self) -> None:
        """Dynamically create bindings for each model ID based on ID_TO_TOPIC."""
        for model_id, _ in ID_TO_TOPIC.items():
            namespace = f"iptc-{model_id}"
            setattr(
                self,
                f"iptc_{model_id}",
                bind(
                    namespace=namespace,
                    version=1,
                    method="POST",
                    endpoint="predict",
                    request_attributes_schema=iptc_v1.PredictRequestAttributeSchemaV1,
                    request_parameters_schema=iptc_v1.PredictRequestParametersSchemaV1,
                    response_attributes_schema=iptc_v1.PredictResponseAttributeSchemaV1,
                ),
            )

    ner = bind(
        namespace="ner",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=ner_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=ner_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=ner_v1.PredictResponseAttributeSchemaV1,
    )

    entity_linking = bind(
        namespace="entity-linking",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=entity_linking_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=entity_linking_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=entity_linking_v1.PredictResponseAttributeSchemaV1,
    )

    topic_summarization = bind(
        namespace="topic-summarization",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=topic_summarization_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=topic_summarization_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=topic_summarization_v1.PredictResponseAttributeSchemaV1,
    )

    topic = bind(
        namespace="topic",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=topic_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=topic_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=topic_v1.PredictResponseAttributeSchemaV1,
    )

    gch_summarization = bind(
        namespace="gch-summarization",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=gch_summarization_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=gch_summarization_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=gch_summarization_v1.PredictResponseAttributeSchemaV1,
    )

    sentiment = bind(
        namespace="sentiment",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=sentiment_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=sentiment_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=sentiment_v1.PredictResponseAttributeSchemaV1,
    )

    lsh = bind(
        namespace="lsh",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=lsh_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=lsh_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=lsh_v1.PredictResponseAttributeSchemaV1,
    )

    iptc_multi = bind(
        namespace="iptc-multi",
        version=1,
        method="POST",
        endpoint="predict",
        request_attributes_schema=iptc_multi_v1.PredictRequestAttributeSchemaV1,
        request_parameters_schema=iptc_multi_v1.PredictRequestParametersSchemaV1,
        response_attributes_schema=iptc_multi_v1.PredictResponseAttributeSchemaV1,
    )

    def __getitem__(self, model: str) -> Any:
        """Dictionary like behaviour to access specific API."""
        model = model.replace("-", "_")
        model_attr = getattr(self, model)
        return model_attr
